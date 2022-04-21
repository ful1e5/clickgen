
Installation
============


Python Support
--------------
clickgen supports these Python versions.

+---------------------+----------+---------+---------+---------+---------+
| **Python**          | **3.10** | **3.9** | **3.8** | **3.7** | **3.6** |
+=====================+==========+=========+=========+=========+=========+
| clickgen 2.0.0      | Yes      | Yes     | Yes     | Yes     |         |
+---------------------+----------+---------+---------+---------+---------+
| clickgen 1.2.0      | Yes      | Yes     | Yes     |         |         |
+---------------------+----------+---------+---------+---------+---------+
| clickgen 1.1.9      |          | Yes     | Yes     |         |         |
+---------------------+----------+---------+---------+---------+---------+
| clickgen 1.1.8      |          | Yes     | Yes     |         |         |
+---------------------+----------+---------+---------+---------+---------+
| clickgen 1.1.7      |          | Yes     | Yes     | Yes     | Yes     |
+---------------------+----------+---------+---------+---------+---------+
| clickgen 1.1.6      |          | Yes     | Yes     | Yes     | Yes     |
+---------------------+----------+---------+---------+---------+---------+
| clickgen 1.1.5beta  |          | Yes     | Yes     | Yes     | Yes     |
+---------------------+----------+---------+---------+---------+---------+
| clickgen 1.1.4beta  |          | Yes     | Yes     | Yes     | Yes     |
+---------------------+----------+---------+---------+---------+---------+
| clickgen 1.1.3beta  |          | Yes     | Yes     | Yes     | Yes     |
+---------------------+----------+---------+---------+---------+---------+
| clickgen 1.1.2beta  |          | Yes     | Yes     | Yes     | Yes     |
+---------------------+----------+---------+---------+---------+---------+
| clickgen 1.1.1beta  |          | Yes     | Yes     | Yes     | Yes     |
+---------------------+----------+---------+---------+---------+---------+
| clickgen 1.1.0beta  |          | Yes     | Yes     | Yes     | Yes     |
+---------------------+----------+---------+---------+---------+---------+


Basic Installation
------------------
Install clickgen with :command:`pip`::

    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade clickgen



Building From Source
--------------------
Download and extract the `compressed archive from PyPI`_.

.. _compressed archive from PyPI: https://pypi.org/project/clickgen/

Building on macOS
^^^^^^^^^^^^^^^^^
To install clickgen with::

    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade clickgen

or from within the uncompressed source directory::

    python3 setup.py install

Building on Linux
^^^^^^^^^^^^^^^^^
If you didn’t build Python from source, make sure you have Python’s development 
libraries installed.

In Debian or Ubuntu::

    sudo apt-get install python3-dev python3-setuptools

In Fedora, the command is::

    sudo dnf install python3-devel redhat-rpm-config

.. Note:: ``redhat-rpm-config`` is required on Fedora 23, but not earlier versions.

To install clickgen with::

    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade clickgen

or from within the uncompressed source directory::

    python3 setup.py install

Platform Support
----------------
Current platform support for clickgen. Binary distributions are contributed for each 
release on a volunteer basis, but the source should compile and run everywhere platform 
support is listed. In general, we aim to support all current versions of Windows, Linux and macOS.

Continuous Integration Targets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
These platforms are built and tested for every change.

+---------------------------------+----------------------------+-------------------------+
| **Operating system**            | **Tested Python versions** | **Tested architecture** |
+---------------------------------+----------------------------+-------------------------+
| Ubuntu Linux 20.04.4 LTS        | 3.7, 3.8, 3.9, 3.10        | x86-64                  |
+---------------------------------+----------------------------+-------------------------+
| macOS 11.6.5                    | 3.7, 3.8, 3.9, 3.10        | x86-64                  |
+---------------------------------+----------------------------+-------------------------+
| Windows Server 2022             | 3.7, 3.8, 3.9, 3.10        | x86-64                  |
+---------------------------------+----------------------------+-------------------------+

.. _release history at PyPI: https://pypi.org/project/clickgen/#history

Old Versions
------------
You can download old distributions from the `release history at PyPI`_ and by direct URL access
eg. https://pypi.org/project/clickgen/1.1.0/.
