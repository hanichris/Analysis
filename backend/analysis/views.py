import asyncio
import hashlib
import hmac
import json
import logging
import os

from asgiref.sync import sync_to_async
from datetime import date
from pathlib import Path
from typing import cast
from uuid import UUID

from django.contrib.auth import aauthenticate, alogin
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator
from django.db import Error
from django.http import (
    Http404,
    HttpRequest,
    HttpResponse,
    HttpResponseNotFound,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import (
    aget_object_or_404, # type: ignore
    redirect,
    render,
)
from django.views.generic import View
from django.views.decorators.http import require_safe

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

from pydantic import ValidationError

from .forms import (
    UploadFileForm,
    UserCreationForm,
    UserEditBirthdayForm,
    UserEditEmailForm,
    UserEditNameForm,
    UserEditPasswordForm,
)
from .config import (
    cancel_sub,
    change_plan,
    get_checkout_url,
    get_user_subscriptions,
    get_subscription_urls,
    pause_sub,
    unpause_sub,
    webhook_has_meta,
)
from .mixins import AsyncLoginRequiredMixin, AsyncUserPassesTestMixin
from .models import (
    Comment,
    Geofield,
    Report,
    Subscription,
    User,
    WebhookEvent,
)
from .serialisers import WebhookEventSerializer
from .tasks import send_to_zoho, process_webhook_event
from .utils import (
    get_plans,
    get_user_phone_number,
    get_user_reports,
    PostData,
    save_report_files,
)

logger = logging.getLogger(__name__)

@api_view(['POST'])
def webhook(request: Request):
    secret = os.getenv('LEMONSQUEEZY_WEBHOOK_SECRET')
    if secret is None:
        return Response(
            'Lemon Squeezy Webhook Secret not set in .env',
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    signature = request.META['HTTP_X_SIGNATURE']
    digest = hmac.new(secret.encode(), request.body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(digest, signature):
        return Response('Invalid signature', status=status.HTTP_400_BAD_REQUEST)

    data = request.data
    if webhook_has_meta(data):
        _data = cast(dict, data)
        serializer = WebhookEventSerializer(
            data={'event_name': _data['meta']['event_name'], 'body': _data}
        )
        if serializer.is_valid():
            event = cast(WebhookEvent, serializer.save())
            process_webhook_event.delay_on_commit(event.pk)
            return Response(status=status.HTTP_200_OK)

    return Response('Invalid data', status=status.HTTP_400_BAD_REQUEST)

@require_safe
def service_worker(request: HttpRequest):
    dir = Path(__file__).parent
    filepath = dir.joinpath('static/analysis/js/serviceWorker.js')
    return HttpResponse(
        filepath.open(encoding='utf-8'),
        headers={
            'Content-Type': 'application/javascript',
            'Service-Worker-Allowed': '/',
        }
    )

@require_safe
async def retrieve_urls(request: HttpRequest, lemonsqueezy_id: str):
    urls = await get_subscription_urls(lemonsqueezy_id)
    return JsonResponse(urls, status=200)

@require_safe
async def pause_subscription(request: HttpRequest, lemonsqueezy_id: str):
    user = cast(User, await request.auser()) # type: ignore
    try:
        await pause_sub(lemonsqueezy_id, user)
        sub = await Subscription.objects.filter(lemonsqueezy_id=lemonsqueezy_id).select_related('plan').aget()
        return render(
            request,
            'analysis/partial.html',
            {
                'subscription': sub,
            }
        )
    except (Subscription.DoesNotExist, RuntimeError):
        raise Http404(f'No subscription with the id: {lemonsqueezy_id} was found.')

@require_safe
async def resume_subscription(request: HttpRequest, lemonsqueezy_id: str):
    user = cast(User, await request.auser()) # type: ignore
    try:
        await unpause_sub(lemonsqueezy_id, user)
        sub = await Subscription.objects.filter(lemonsqueezy_id=lemonsqueezy_id).select_related('plan').aget()
        return render(
            request,
            'analysis/partial.html',
            {
                'subscription': sub,
            }
        )
    except (Subscription.DoesNotExist, RuntimeError):
        raise Http404(f'No subscription with the id: {lemonsqueezy_id} was found.')

@require_safe
async def cancel_subscription(request: HttpRequest, lemonsqueezy_id: str):
    user = cast(User, await request.auser()) # type: ignore
    try:
        await cancel_sub(lemonsqueezy_id, user)
        sub = await Subscription.objects.filter(lemonsqueezy_id=lemonsqueezy_id).select_related('plan').aget()
        return render(
            request,
            'analysis/partial.html',
            {
                'subscription': sub,
            }
        )
    except (Subscription.DoesNotExist, RuntimeError):
        raise Http404(f'No subscription with the id: {lemonsqueezy_id} was found.')

class IndexView(View):
    parents = Path(__file__).parents
    new_path = parents[1].joinpath('static/manifest.json')
    with new_path.open(encoding='utf-8') as fd:
        manifest: dict = json.load(fd)

    async def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request,
            "analysis/home.html",
            {
                "manifest": self.manifest.get("src/main.tsx"),
            }
        )
    
    async def post(self, request: HttpRequest, *args, **kwargs):
        try:
            data = PostData(**json.loads(request.body.decode('utf-8')))
            await Comment.objects.acreate(**data.model_dump())
            send_to_zoho.delay(data.model_dump())

        except ValidationError as err:
            logger.error(err)
            return JsonResponse({
                "msg": "Validation of the data failed.",
                "type": "error",
            }, status=400)
        except Error as err:
            logger.error(err)
            return JsonResponse({
                "msg": "An error occurred while saving your message.",
                "type": "error",
            }, status=500)
        else:
            return JsonResponse({
                "msg": "Your message has been saved",
                "type": "success"
            }, status=201)

class DashboardView(AsyncLoginRequiredMixin, View):
    
    access_token = os.getenv('MAPBOX_ACCESS_TOKEN')

    async def get(self, request: HttpRequest, *args, **kwargs):
        user = cast(User, await request.auser()) # type: ignore
        return render(
            request,
            "analysis/dashboard.html",
            {
                "access_token": self.access_token,
                "user": user
            }
        )

class Coordinates(View):
    content = {
        'content': [],
        'error': None, 
        'msg': '',
        'op': '',
        'success': None,
    }

    async def get(self, request: HttpRequest, *args, **kwargs):
        pk = self.kwargs['pk']
        qs = Geofield.objects.filter(user__pk=pk)
        self.content['msg'] = 'Successfully retrieved data from the database'
        self.content['op'] = 'GET'
        self.content['success'] = True
        self.content['content'] = [
            {
                'geometry': entry.geometry,
                'id': cast(str, entry.unique_id).rsplit(',', 1)[-1],
                'properties': {},
                'type': 'Feature',
            }
            async for entry in qs
        ]
        return JsonResponse(self.content, status=200)

    async def post(self, request: HttpRequest, *args, **kwargs):
        pk = self.kwargs['pk']
        data: dict = json.loads(request.body.decode('utf-8'))
        user = await User.people.aget(pk=pk)
        create_data = [
            Geofield(
                user=user,
                feature_id=feature["feature_id"],
                geometry=feature["geometry"]
            )
            for feature in data['features']
        ]

        created_objects = await Geofield.objects.abulk_create(
            create_data,
            update_conflicts=True, # type: ignore
            update_fields=["geometry"],
            unique_fields=["unique_id"]
        )

        self.content['msg'] = 'Successfully saved the coordinates into the database'
        self.content['op'] = "POST",
        self.content['success'] = True,
        self.content['content'] = [
            {
                'geometry': item.geometry,
                'id': cast(str, item.unique_id).rsplit(',', 1)[-1],
                'properties': {},
                'type': 'Feature',
            }
            for item in created_objects
        ]
        return JsonResponse(self.content, status=200)

class SignUpView(View):
    async def get(self, request: HttpRequest, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'registration/signup.html', {'form': form})

    async def post(self, request: HttpRequest, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if await sync_to_async(form.is_valid)():
            await sync_to_async(form.save)()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = await aauthenticate(request, email=email, password=password)
            await alogin(request, user)
            # Set up email verification
            return redirect('/billing/')
        return render(
            request, 'registration/signup.html', {'form': form}
        )


# class SignUpView(CreateView):
#     form_class = UserCreationForm
#     model = User
#     success_url = reverse_lazy('login')
#     template_name = "registration/signup.html"

class UserProfileView(AsyncLoginRequiredMixin, View):
    async def get(self, request: HttpRequest, *args, **kwargs):
        user= cast(User, await request.auser()) # type: ignore

        async with asyncio.TaskGroup() as tg:
            report_task = tg.create_task(get_user_reports(user))
            sub_task = tg.create_task(get_user_subscriptions(user))
            number_task = tg.create_task(get_user_phone_number(user))
        reports = report_task.result()
        number = number_task.result()
        subscriptions = sub_task.result()

        page_number = request.GET.get('page')
        paginator = Paginator(reports, 3)
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj': page_obj,
            'user': user,
            'phone_number': None,
            'subscriptions': subscriptions,
        }
        if number:
            context['phone_number'] = number
        return render(
            request,
            'analysis/profile.html',
            context
        )

class UserProfileEditView(AsyncLoginRequiredMixin, View):
    async def get(self, request: HttpRequest, *args, **kwargs):
        user= cast(User, await request.auser()) # type: ignore
        field = request.GET.get('field')
        title = ''
        form = None
        match(field):
            case 'name':
                title = 'name'
                form = UserEditNameForm(initial={
                    'first_name': user.first_name.capitalize() if user.first_name else '',
                    'last_name': user.last_name.capitalize() if user.last_name else '',
                })
            case 'birthday':
                title = 'birthday'
                form = UserEditBirthdayForm(initial={
                    'month': user.birth_date.month if user.birth_date else '',
                    'day': user.birth_date.day if user.birth_date else '',
                    'year': user.birth_date.year if user.birth_date else '',
                })
            case 'email':
                title = 'email'
                form = UserEditEmailForm(initial={'email': user.email})
            case 'password':
                title = 'password'
                form = UserEditPasswordForm()
            case _:
                return HttpResponseNotFound()
        return render(
            request,
            'analysis/edit.html',
            {
                'form': form,
                'title': title,
                'user': user,
            }
        )

    async def post(self, request: HttpRequest, *args, **kwargs):
        user= cast(User, await request.auser()) # type: ignore
        field = request.POST.get('field')
        form = None
        title = ''
        match(field):
            case 'name':
                title = 'name'
                form = UserEditNameForm(request.POST)
            case 'birthday':
                title = 'birthday'
                form = UserEditBirthdayForm(request.POST)
            case 'email':
                title = 'email'
                form = UserEditEmailForm(request.POST)
            case 'password':
                title = 'password'
                form = UserEditPasswordForm(request.POST)
            case _:
                return HttpResponseNotFound()
        
        if form.is_valid():
            match(field):
                case 'name':
                    user.first_name = cast(str, form.cleaned_data['first_name']).lower()
                    user.last_name = cast(str, form.cleaned_data['last_name']).lower()
                case 'birthday':
                    day = form.cleaned_data['day']
                    month = form.cleaned_data['month']
                    year = form.cleaned_data['year']
                    iso_date = f"{year:0>4}-{month:0>2}-{day:0>2}"
                    user.birth_date = date.fromisoformat(iso_date)
                case 'email':
                    user.email = form.cleaned_data['email']
                case 'password':
                    user.set_password(form.cleaned_data['password1'])
                case _:
                    return HttpResponseNotFound()
            await user.asave()
            if field == 'password':
                # Updating the password logs out the current user from existing session.
                # Thus, log them back in. Provided functions do not work as intended.
                await alogin(request, user)
                # await sync_to_async(update_session_auth_hash)(request, user)
                # await aupdate_session_auth_hash(request, user)
        else:
            return render(
                request,
                'analysis/edit.html',
                {
                    'form': form,
                    'title': title,
                    'user': user,
                }
            )
        return HttpResponseRedirect(f'/users/{user.id}/')


class UploadReport(AsyncLoginRequiredMixin, AsyncUserPassesTestMixin, View):
    async def get(self, request: HttpRequest, *args, **kwargs):
        return render(
            request,
            "analysis/upload.html",
            {
                'form': UploadFileForm(),
            }
        )
    
    async def post(self, request: HttpRequest, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = await aget_object_or_404(User, email=email)
            await save_report_files(user, form.cleaned_data['file'])
        else:
            return render(
                request,
                'analysis/upload.html',
                {
                    'form': form
                }
            )
            
        return render(
            request,
            "analysis/upload.html",
            {
                'form': UploadFileForm(),
            }
        )

async def download_file(request, pk: int):
    uploaded_file = await Report.objects.aget(pk=pk)
    print(uploaded_file.file.name)

class Billing(AsyncLoginRequiredMixin, View):
    async def get(self, request: HttpRequest, *args, **kwargs):
        user = cast(User, await request.auser()) # type: ignore
        plans = await get_plans()
        if plans:
            async with asyncio.TaskGroup() as tg:
                tasks = [
                    tg.create_task(get_checkout_url(plan.variant_id, user))
                    for plan in plans
                ]
            urls = [task.result() for task in tasks]
            plans = zip(plans, urls)
        return render(
            request,
            'analysis/billing.html',
            {
                'plans': plans,
            }
        )

class ChangeBilling(AsyncLoginRequiredMixin, View):
    async def get(self, request: HttpRequest, *args, **kwargs):
        user = cast(User, await request.auser()) # type: ignore
        plan_id = cast(int, self.kwargs['pk'])

        async with asyncio.TaskGroup() as tg:
            plans_task = tg.create_task(get_plans())
            subs_task = tg.create_task(get_user_subscriptions(user))
        user_subs: list[Subscription] = subs_task.result()
        plans = plans_task.result()

        current_sub = cast(
            Subscription | None,
            next(filter(lambda x: x.plan.pk == plan_id, user_subs), None))
        if current_sub is None:
            raise Http404(f'Plan with id {plan_id} was not found!')
        
        if plans is None:
            return redirect('analysis:billing')
        
        return render(
            request,
            'analysis/change_plan.html',
            {
                'plans': plans,
                'current_sub': current_sub,
            }
        )
    
    async def post(self, request: HttpRequest, *args, **kwargs):
        user = cast(User, await request.auser()) # type: ignore
        current_plan_id = cast(int, self.kwargs['pk'])
        new_plan_id = int(request.META['HTTP_X_NEW_PLAN'])
        try:
            await change_plan(current_plan_id, new_plan_id, user)
            return redirect(f'/users/{user.pk}/')
        except RuntimeError as exc:
            raise Http404(exc)