**Kuvien is now a dead project. This API interface will no longer work for its intended use.**

pykuvien
========

The official API interface for `kuvien.io <https://kuvien.io>`_.

Example:

.. code-block:: python

  from pykuvien import Api

  api = Api('mykeyhere')

  valid_domains = api.domains()
  api.add_subdomain('my', valid_domains[3])


You can use this API to manage your account, and upload images.
