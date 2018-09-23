# docker-django-webpack-skeleton v2.0.2
Django Skeleton W/ Docker Dev & Production W/ Webpack W/ BabelJS W/ Sass W/ PostgreSQL by @phpdude
forked by @iddevelper

You can bootstrap your next django project with command

> django-admin.py startproject --template=https://github.com/iddevelper/docker-django-webpack-skeleton/archive/master.zip -e "ini,yml,conf,json" yoursite

You can use Fabric to deploy your project to any docker supported env.

> fab build deploy

You can run local development environment with 

> docker-compose up

You can make a pull request if you like project and ready to help with documentation.

Quick start:
> docker-compose build 
> docker-compose run manage migrate 
> docker-compose run createsuperuser
> docker-compose up

What's New:
-image debian:stable-slim -> python:latest
-setup timezone "Europe/Moscow"
-config 443 port in production