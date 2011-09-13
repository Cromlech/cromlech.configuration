#!/usr/bin/python

from zope.component import hooks
from zope.interface import implements
from zope.configuration import xmlconfig, config
from zope.security.management import newInteraction, endInteraction
from zope.security.interfaces import IParticipation
from zope.security.management import system_user


class SystemConfigurationParticipation(object):
    implements(IParticipation)

    principal = system_user
    interaction = None


def load_zcml(file, features=(), execute=True):
    r"""Execute the ZCML configuration file.

    This procedure defines the global site setup. Optionally you can also
    provide a list of features that are inserted in the configuration context
    before the execution is started.

    Let's create a trivial sample ZCML file.

      >>> import tempfile
      >>> fn = tempfile.mktemp('.zcml')
      >>> zcml = open(fn, 'w')
      >>> zcml.write('''
      ... <configure xmlns:meta="http://namespaces.zope.org/meta"
      ...            xmlns:zcml="http://namespaces.zope.org/zcml">
      ...   <meta:provides feature="myFeature" />
      ...   <configure zcml:condition="have myFeature2">
      ...     <meta:provides feature="myFeature4" />
      ...   </configure>
      ... </configure>
      ... ''')
      >>> zcml.close()

    We can now pass the file into the `config()` function:

      # End an old interaction first
      >>> from zope.security.management import endInteraction
      >>> endInteraction()

      >>> context = config(fn, features=('myFeature2', 'myFeature3'))
      >>> context.hasFeature('myFeature')
      True
      >>> context.hasFeature('myFeature2')
      True
      >>> context.hasFeature('myFeature3')
      True
      >>> context.hasFeature('myFeature4')
      True

    Let's now clean up by removing the temporary file:

      >>> import os
      >>> os.remove(fn)

    """
    # Set user to system_user, so we can do anything we want
    newInteraction(SystemConfigurationParticipation())

    try:

        # Hook up custom component architecture calls
        hooks.setHooks()

        # Load server-independent site config
        context = config.ConfigurationMachine()
        xmlconfig.registerCommonDirectives(context)
        for feature in features:
            context.provideFeature(feature)
        context = xmlconfig.file(file, context=context, execute=execute)

    finally:
        # Reset user
        endInteraction()
