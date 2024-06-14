# Analysis
A web application that provides land analysis to farmers

## Usage
### Set up a virtual environment.
To ensure that you do not mess up your local python dependencies, clone this repo into
a python virtual environment. You can use ``venv`` or ``pyenv`` to manage your virtual environments.  

### Install dependencies
With your environment set up, run the following command in your terminal:    
   
```
python3 -m pip install -r requirements.txt
```  
  
### Database migrations
With your dependencies installed, change your current working directory to the directory with the ``manage.py`` file. Once in that directory, run the following command in your terminal:   
  
```
python manage.py migrate
```  
  
### Create an admin user
You will need to create a user who can login into to the admin site. Run the following command:   
   
```
python manage.py createsuperuser
```  
   
Follow the prompts presented to you.


### Build the react frontend.
To ensure the react frontend can be server-side rendered, run the following command to build the frontend:   
If you are using ``pnpm`` as your package manager:   
    
```
pnpm build
```    
    
If you are using ``npm``, then the command to run would be:    
   
```
npm run build
```   
   

### Start the development server.
Doing so requires running the following command:  
    
```
python manage.py runserver
```    

