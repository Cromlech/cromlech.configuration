#!/usr/bin/python

from zope.configuration import xmlconfig, config


def load_zcml(file, features=(), execute=True):
    r"""Execute the ZCML configuration file.

    This procedure defines the global site setup. Optionally you can also
    provide a list of features that are inserted in the configuration context
    before the execution is started.

    Let's create a trivial sample ZCML file.

      >>> import tempfile
      >>> fn = tempfile.mktemp('.zcml')
      >>> zcml = open(fn, 'w')
      >>> assert zcml.write('''
      ... <configure xmlns:meta="http://namespaces.zope.org/meta"
      ...            xmlns:zcml="http://namespaces.zope.org/zcml">
      ...   <meta:provides feature="myFeature" />
      ...   <configure zcml:condition="have myFeature2">
      ...     <meta:provides feature="myFeature4" />
      ...   </configure>
      ... </configure>
      ... ''')
      >>> zcml.close()

    We can now pass the file into the `load_zcml()` function:

      >>> context = load_zcml(fn, features=('myFeature2', 'myFeature3'))
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
    # Load server-independent site config
    context = config.ConfigurationMachine()
    xmlconfig.registerCommonDirectives(context)
    for feature in features:
        context.provideFeature(feature)
    context = xmlconfig.file(file, context=context, execute=execute)
    return context
