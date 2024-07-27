import { ZodError, ZodType } from "zod";

type ZObjectType = ZodType<Record<string | number, unknown>>;

type ZodParams<T extends ZObjectType> = {
  onSuccess(data: T['_output'], timeout?: number): void;
  onError(error: Partial<Record<keyof T['_output'], string>>): void;
  data: Record<string, unknown>;
  schema: T;
};

const handleZodError = ({ issues }: ZodError<unknown>) => {
  const errorMessages: Record<string, string> = {};

  if (issues.length === 1 && issues[0].path.length < 1) {
    return issues[0].message;
  }
  
  issues.forEach(({ path, message }) => {
    errorMessages[path.join('-')] = message;
  });
  return errorMessages;
};

export const handleZodValidation = <T extends ZObjectType>(params: ZodParams<T>) => {
  const { data, onSuccess, onError, schema} = params;

  try {
    const res = schema.parse(data);
    onSuccess(res);
  } catch (error) {
    if (error instanceof ZodError) {
      const formattedError = handleZodError(error);
      onError(formattedError as Record<keyof T['_output'], string>);
    } else {
      throw new Error(String(error));
    }
  }
};

export type ValidationError<T extends ZObjectType> = Partial<Record<keyof T['_output'], string>>;