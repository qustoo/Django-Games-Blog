###########
# BUILDER #
###########

FROM python:3.10-alpine AS app_builder


ENV PYTHONDONTWRITEBYTECOD=1
ENV PYTHONUNBUFFERED=1
ENV SRC_APP=/src/app

WORKDIR $SRC_APP

RUN apk update \
    && apk add postgresql-dev gcc python3-dev
RUN pip install --upgrade pip
# musl-dev

COPY ./requirements.txt $SRC_APP
RUN pip wheel --no-cache-dir --no-deps --wheel-dir $SRC_APP/wheels -r requirements.txt

#########
# FINAL #
#########
FROM app_builder

RUN addgroup -S app_group && adduser -S app_user -G app_group

ENV APP_HOME=/app
WORKDIR $APP_HOME
RUN mkdir $APP_HOME/static
RUN mkdir $APP_HOME/media

RUN apk update && apk add libpq
COPY --from=app_builder /src/app/wheels /wheels
COPY --from=app_builder /src/app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY entrypoint.sh $APP_HOME

COPY . $APP_HOME

RUN chown -R app_user:app_group $APP_HOME

USER app_user

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]