=====
Usage
=====

This tutorial is intended as an introduction to work with ``os-acc``.

Prerequisites
-------------

Before we start, make sure that you have the **os-acc** distribution
:doc:`installed </install/index>`.To begin using the library, first call
the os_acc module. This will load all installed plugins and register the
object mode.

.. code-block:: bash

   >>> import os_acc

Nova Compute - Os-acc API
-------------------------
The following example shows how Nova Compute calls the os-acc APIs if it sees
that the requested flavor refers to CUSTOM_ACCELERATOR_* resource classes.
The APIs are called asynchronously, as suggested below:

.. code-block:: python

   with ThreadPoolExecutor(max_workers=N) as executor:
      future = executor.submit(os_acc.<api>, *args)
      # ... do other stuff ...
      try:
         data = future.result()
      except:
         # handle exceptions

Once the ``os_acc`` library is initialized, there are only two other library
functions: ``os_acc.acquire_accelerators_for_instance()`` and
``os_acc.release_accelerators_for_instance()``. Both methods accept an
argument of instance_info: Nova's per-instance versioned object, while
acquire_accelerators_for_instance() method requires another two arguments:
extra_specs which describs the extra_specs field in the flavor, including
fields interpreted by Cyborg but not Nova, and device_rp[].

.. code-block:: python

   import os_acc
   from os_acc import exception as acc_exc
   import uuid

   from nova import objects as nova_objects

   instance_uuid = 'd7a730ca-3c28-49c3-8f26-4662b909fe8b'
   instance = nova_objects.Instance.get_by_uuid(instance_uuid)
   instance_info = instance_info.InstanceInfo(
       uuid=instance.uuid,
       name=instance.name,
       project_id=instance.project_id)

    # Now do the actual operations to attach the accelerator to
    # an instance
    try:
        os_acc.acquire_accelerators_for_instance(self, device_rp[],
             extra_specs, instance_info)
    except acc_exc.PlugException as err:
    # handle the failure

    # Now do the actual operations to detach the accelerator to
    # an instance
    try:
        os_acc.release_accelerators_for_instance(self, instance_uuid)
    except acc_exc.UnplugException as err:
    # handle the failure

    # Hot add/remove of accelerators from running VM is for future

