.. _to10.0_asyncio:

==============================================
Deprecation of sync methods in Asyncio servers
==============================================

Historically, the implementation of green_modes utilized the basic sync PyTango code and
tried to convert in on the fly to async. The main advantage of such implementation is simple code maintaining:
all changes we make automatically applied to all green modes.

However, with Asyncio mode there is a major problem:
to convert all original sync method we used asyncio.coroutine function,
which was the first iteration to make coroutines by asyncio. Unfortunately, it  was deprecated in Python 3.8
and finally removed from Python 3.11.

As the temporary solution we copied asyncio.coroutine code to PyTango.
But then cleaning process of Asyncio library continued and for Python 3.12 we
had to copy run_coroutine_threadsafe and modify it to be able to work with such legacy generator-based coroutines.

Since there is no guarantee, that our copied methods will be compatible
with new versions of Asyncio we decided to change, how Asycnio mode of pytango is implemented:

**Starting from PyTango 10.0.0 all Asyncio servers should be from the beginning written with "async def" methods.**
The base Device class was also modified to be written with "async def", so instead of
doing "super().<method name>()" calls you **must** do "await super().<method name>()"

In PyTango 10.0.0 we still preserve option to run legacy servers, with sync user functions,
but every time server is started you will become DeprecationWarning.
