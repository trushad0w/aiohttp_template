# aiohttp_template

Python clean architecture approach for aiohttp

# Common
I'll start with common features that are designed to make development process easier.

## 1. api module
This module contains basic middleware to handle errors all over the project,
also this module provides handy decorator for your views `definition`. 

### _definition decorator_

This decorator allows you to define route paths and their validation schemas 
right above the view function, additionally it helps you to keep all response formats same 
by using `response`, `response_error` and `response_pagination` methods defined 
in _api->declaration->factory_.

Then, all you need is to setup routes calling `setup_routes` from `__init__.py`. 
Example provided in _config->routes.py_.

Also this decorator generates swagger documentation for your routes and makes it available 
here `http://<host>:<port>/swagger.json`

### exceptions.py
Basic exceptions for API are described here, their instances are handled in error_handler.py middleware

## 2. db module

Here you can find connection pools initializers for main databases 
(mongodb, mysql, postgresql).

Each connector can manage several database pools with their own connection pool sizes.

Usage example for mongo db initialization provided here _manage.py->init_app()_.
Usage example for db requests can be found here _apps->posts->repositories_.

This module makes db connection visible in global scope and there are no boundaries 
to aiohttp framework.

## 3. services module
This module manages operations with external services.

`ClientSession` and `ServiceClient` classes in _services->client.py_ are necessary 
for dependent clients. They provide easier initialization, and methods with extended 
functionality to correctly maintain and dispose connections to external services.

This module is designed in such way that you can split your client in separate libraries 
and reuse them in any other project. app_pages is an example of such library that can 
be separated in the future.

_config->external.py_ provides you an example of external services initialization. 
Then this method is called on app init.

_apps->posts->services->posts.py->`PostsService`->`external_service_example()`_ 
this method is an example of the external client usage

## 4. base_dto.py

This file contains base class for dataclasses all over the project. 
It's used to create dataclasses or classes from dict by calling `make()` method.
It has `asdict()` method to convert your objects into dict again.

DTO are used for data transfering between layers of your application.

## 5. health_check.py

Just a route to handle health checks.

## 6. logger

Logger for the project. You need to setup it on app init by passing log_level into
`init_logger()` method. Then all that you need is just import app_logger from this 
module to log necessary information.

# Config

Here we have: 
* `remote_config.py` - for consul variables management.
* `routes.py` - for app routing setup.
* `external.py` - for external services setup.
* `settings.py` - project's settings.

`set_env_vars()` method that is called in the settings helps you to make local development
 easier. Because it doesn't matter where your variables are stored, consul, env_variables or `.env` file.
 This setup will do it's job in any case.

# manage.py

Consists of application setup and run methods, also provides method to perform 
db migration operations

# migrations

There are no naming rules for this folders, there are 2 examples of sql 
and nosql migrations, and cuz of that, they called here pg_migrate and mongo_migrations.

In any other case there should be only one maintainable storage per project, 
so usually you call folder with migrations as `migrations`.  

Helper methods in manage.py `mongo_migrate()` and `pg_migrate` 
should be renamed to just `migrate`.

On every app deploy migration operations must be run as a step before deploy.

If there are no migrations to apply this step will be automatically skipped.


# apps

So, every app usually consists of several layers such as:
1. Views
2. Services
3. Repositories

Each of this layer has it's own rules.

**Views** - can perform operations that affects input and output data view.
In other words this layer can perform input data validation operations  
and data formatting operations (which can be achieved in most scenarios with `schemas`).
Views can interact with service layer and nothing more.

**Services** - contains all the business logic of your app. 
It can interact with other services, external services and repositories.

**Repositories** - Just data gathering layer. Only performs operations with data source
and nothing more.
No business logic should be described here. Can only interact with data source.

#### **Helpers:**

Usually it's quite convenient to transfer preprocessed data between those layers.
And here is when DTO comes into place.
They are described in the `models` module. This dataclasses can help you and 
your teammates to understand what's going on with your data 
and what to expect after calling some method in your class.
And this little datastructures make your code much more clean for the others.

