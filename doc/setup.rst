#####
Setup
#####

#. Install.

   `Install Rspamd
   <https://rspamd.com/doc/quickstart.html#rspamd-installation>`_ on your server.
   It is advised to apply recommended changes to the Redis configuration.

   Then install modoboa-rspamd in you venv::

      sudo -u <modoboa_user> -i bash
      source <venv_path>/bin/activate
      pip install modoboa-rspamd

   You then need to add `modoboa_rspamd` to `MODOBOA_APPS`::

      MODOBOA_APPS = (
      ....
      # Modoboa extensions here.
      'modoboa_rspamd',
      )


#. Proxy setup.

   In order for rspamd to communicate with postfix, you must
   enable the `proxy worker <https://rspamd.com/doc/workers/rspamd_proxy.html>`_
   and perhaps disable the normal worker to save resources.

   Then you need to edit postfix configuration to re-route mails to rspamd milter.

   #. DKIM setup.

   It is recommended to create a "dkim" user and add it to both _rspamd and modoboa group.
   If you want to fine tune the permission, modoboa needs read/write and _rspamd only read.

   The map updating process is automatically done in the background using RQ (starting modoboa 2.2.0).
   Please take a look at the RQ instructions on modoboas main documentation. You only need to change
   the user for the supervisord ini file.

   Then, go to the *Modoboa > Parameters > Rspamd* panel and edit the
   **Path map path** and **Selector map path** settings if necessary
   (an absolute path is required and modoboa user must have write permission on it).


   Then update Rspamd dkim signing configuration (should be here : /etc/rspamd/local.d/dkim_signing.conf):

      .. code :

      try_fallback = false;
      selector_map = "**Path map path** ";
      path_map = "**Selector map path**";


   When the configuration is done, Modoboa will completly handles the
   updates when DKIM is changed on a domain.


#. Other settings.

   You can take a look at the `configuration files
   <https://github.com/modoboa/modoboa-installer/tree/master/modoboa_installer/scripts/files>`_
   available on `modoboa_installer <https://github.com/modoboa/modoboa-installer>`_.
   Keep in mind, this is just a recommended configuration.
