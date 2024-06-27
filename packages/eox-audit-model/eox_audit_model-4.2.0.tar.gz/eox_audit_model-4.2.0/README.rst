==========================
Django eduNEXT Audit Model
==========================

.. image:: https://github.com/eduNEXT/eox-audit-model/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/eduNEXT/eox-audit-model/actions/workflows/tests.yml


.. image:: https://github.com/eduNEXT/eox-audit-model/actions/workflows/bump_version.yml/badge.svg
    :target: https://github.com/eduNEXT/eox-audit-model/actions/workflows/bump_version.yml

.. image:: https://github.com/eduNEXT/eox-audit-model/actions/workflows/python-publish.yml/badge.svg
    :target: https://github.com/eduNEXT/eox-audit-model/actions/workflows/python-publish.yml

.. image:: https://img.shields.io/badge/Status-Maintained-brightgreen

Installation
############

1. Install eox-audit-model:

    .. code-block:: python

      pip install eox-audit-model

2. Add “eox_audit_model” to your INSTALLED_APPS:

    .. code-block:: python

      INSTALLED_APPS = [
              ...
            'eox_audit_model',
      ]

3. Run Migrate:

    .. code-block:: python

      python manage.py migrate eox_audit_model

Open edX compatibility notes
----------------------------

+------------------+---------------+
| Open edX Release | Version       |
+==================+===============+
| Juniper          | >=0.2, < 0.4  |
+------------------+---------------+
| Koa              | >=0.4, <= 0.7 |
+------------------+---------------+
| Lilac            | >=0.4, <= 0.7 |
+------------------+---------------+
| Maple            | >=0.7, <1.0   |
+------------------+---------------+
| Nutmeg           | >=1.0         |
+------------------+---------------+
| Olive            | >=2.0         |
+------------------+---------------+
| Palm             | >=3.0         |
+------------------+---------------+
| Quince           | >=4.0         |
+------------------+---------------+
| Redwood          | >=4.2.0       |
+------------------+---------------+


Usage
#####
Audit any execution of a method or function. This will create a database register with the following information:

1. Status. If the process was successful or not.
2. Action. The string given to identify the process.
3. Time stamp. The execute date.
4. Method name. Method or function name.
5. Captured log. logs generated in the execution.
6. Traceback log. If there was an exception, this will contain the traceback.
7. Site. Current site.
8. Performer. The user who started the method, this depend on the request.user
9. Input. The values used to execute the method.
10. Output. The value returned by the method.
11. Ip. Current ip.

- Example:

.. code-block:: python

  from eox_audit_model.models import AuditModel

  def any_method(parameter1, parameter2, parameter3):
    """Do something"""
    return 'Success'

  def audit_process():
    """Execute audit process"""
    action = "This is a simple action"
    parameters = {
      "args": (2, 6),
      "kwargs": {"parameter3": 9},
    }

    expected_value = AuditModel.execute_action(action, any_method, parameters)
    ...

Decorator
#########
There is a simple decorator, which can perform the same process.

- Example:

.. code-block:: python

  from eox_audit_model.decorators import audit_method

  @audit_method(action="This is a simple action")
  def any_method(parameter1, parameter2, parameter3):
    """Do something"""
    return 'Success'

  def audit_process():
    """Execute audit process"""
    expected_value = any_method(3, 6, 9)
    ...


Contributing
############

Add your contribution policy. (If required)
