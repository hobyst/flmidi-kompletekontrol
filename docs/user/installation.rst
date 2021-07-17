============
Installation
============

.. note::

	If at any point following this installation guide you come across problems, then refer to the
	:ref:`troubleshooting` section at the end of this page.


.. _introduction:

Introduction
============

The Komplete Kontrol keyboards by themselves work just fine as a standard MIDI device on any device
that supports MIDI over USB. But the deep integration features for DAWs require an additional MIDI device
that is only created by the Native Instruments drivers that come bundled with the Komplete Kontrol software
when they detect a keyboard has been connected to the host computer. In order to properly understand the
installation process this section will go through the different MIDI devices that need to be present and how
to identify them in order to get the script working.

MIDI keyboard
	This MIDI device is created by the keyboard itself and will appear in any device and OS
	compatible with MIDI over USB. This device represents the lower half of the keyboard inlcuding keypressings,
	mod and pitch wheels, the touchstrip (S-Series) and the knobs in MIDI mode.

DAW control surface
	This MIDI device is created by the Native Instruments drivers when a Komplete Kontrol keyboard is detected.
	It represents the upper half of the keyboard and it's the MIDI port DAWs connect with to get the DAW integration
	features working on the keyboard. All the DAW integration scripts and configurations should be assigned
	to this MIDI port.

Integrated MIDI interface (S-Series only)
	S-Series keyboards have an integrated MIDI interface in order to forward messages from the 5-pin MIDI input
	and output ports found on the back of the keyboard. This MIDI port is what forwards the messages of the device
	that got connected to the keyboard to your computer, making the keyboard act as a bridge between the two.

Depending on the Komplete Kontrol device, the amount of MIDI devices and their names vary:

.. table:: **S-Series MK2 MIDI devices scheme**

  +-------------------+-------------------------------+
  | Device type       | Name                          |
  +===================+===============================+
  | MIDI keyboard     | ``KOMPLETE KONTROL - 1``      |
  +-------------------+-------------------------------+
  | DAW control       | ``Komplete Kontrol DAW - 1``  |
  | surface           |                               |
  +-------------------+-------------------------------+
  | Integrated        |  ``KOMPLETE KONTROL EXT - 1`` |
  | MIDI interface    |                               |
  +-------------------+-------------------------------+

.. table:: **A-Series MIDI devices scheme**

  +-------------------+-------------------------------+
  | Device type       | Name                          |
  +===================+===============================+
  | MIDI keyboard     | ``KOMPLETE KONTROL <MODEL>    |
  |                   | MIDI``                        |
  |                   |                               |
  |                   | Where ``<MODEL>`` is either   |
  |                   | ``A25``, ``A49`` or ``A61``   |
  +-------------------+-------------------------------+
  | DAW control       | ``Komplete Kontrol A DAW``    |
  | surface           |                               |
  +-------------------+-------------------------------+

.. table:: **M32 MIDI devices scheme**

  +-------------------+-------------------------------+
  | Device type       | Name                          |
  +===================+===============================+
  | MIDI keyboard     | ``KOMPLETE KONTROL M32 MIDI`` |
  +-------------------+-------------------------------+
  | DAW control       | ``Komplete Kontrol M DAW``    |
  | surface           |                               |
  +-------------------+-------------------------------+


.. important::
  Pay close attention to the naming of the different MIDI devices, specially on the S-Series MK2 keyboards. All devices are
  named similarly and it's really easy to confuse one with the others.


Requirements
============

- FL Studio 20.8.3 or greater

  - Released on March 31st, 2021
  - Windows build 20.8.3.2304
  - macOS build 20.8.3.1574
  - MIDI Scripting API version 11

- Komplete Kontrol 2.3.0 or greater
- Download the latest firmware for your device on the `Drivers <https://www.native-instruments.com/en/support/downloads/drivers-other-files/>`__ page.
- If there are any standalone drivers for your device, download and install them as well.

Download the script
======================

You can go to the `Releases <https://github.com/hobyst/flmidi-kompletekontrol/releases>`__ download to the ``Native-Instruments-Komplete-Kontrol.zip`` asset
(as well as this manual) from the latest release and extract the ``.zip`` file on the FL Studio MIDI scripts folder inside your Image-Line User Data folder, located on:

- Windows: ``Documents\Image-Line\FL Studio\Settings\Hardware\``
- macOS: ``Documents/Image-Line/FL Studio/Settings/Hardware/``

.. tip::

  The paths above for the MIDI scripts folder are given assuming the default location for the Image-Line User Data folder,
  which is inside the Documents folder of your Windows or macOS user. If you have issues finding it, you can always open FL Studio,
  go to ``Options > File settings`` and look at the ``User data folder`` setting. From there, go to ``FL Studio/Settings/Hardware``
  and that's it.

But if you want a more automated install and update process, you can use Git and a terminal:

1. Download and install `Git <https://git-scm.com/downloads>`__

2. Open a terminal and run line by line:
   
   - Windows:
					.. code-block:: batch

							cd "%USERPROFILE%\Documents\Image-Line\FL Studio\Settings\Hardware"

							git clone --recursive https://github.com/hobyst/flmidi-kompletekontrol.git "Native Instruments Komplete Kontrol"

   - macOS:
					.. code-block:: bash

							cd "~/Documents/Image-Line/FL Studio/Settings/Hardware"

							git clone --recursive https://github.com/hobyst/flmidi-kompletekontrol.git "Native Instruments Komplete Kontrol"

.. tip::

		The ``cd`` command on a terminal is used to change the directory you are running commands on. If the path for your
		Image-Line User Data folder isn't the default one, change the path next to the ``cd`` word to match your Image-Line
		User Data folder path. To avoid errors, keep the path between quote symbols (``""``).

Indifferently of whatever installation method you used, the folder structure inside the Hardware folder should look like this:

- ...

- ``Native Instruments Komplete Kontrol/``

  - ``.git/`` (this folder will appear if you used the Git method)
  - ``nihia/``

    - ...
    - ``__init__.py``
    - ``buttons.py``
    - ``mixer.py``
    - ...

  - ...
  - ``config.py``
  - ``controller_definition.py``
  - ``device_Komplete Kontrol (S-Series Custom MIDI Map).py``
  - ``device_KompleteKontrol.py``
  - ``midi_setup_check.py``
  - ``mixer_definition.py``
  - ...

- ...

.. tip::

		If the ``nihia`` folder is empty, then you got the wrong asset file from the Releases page or you run ``git clone``
		without the ``--recursive`` argument.

Assign the script to the device inside FL Studio
================================================

.. note::
   The following section contains screenshots and GIF animations for exemplification purposes
   that reflect the MIDI device list on FL Studio when a Komplete Kontrol A61
   keyboard is connected to a computer and drivers are properly installed.

   To check the MIDI device names that match your Komplete Kontrol model, please
   check the :ref:`introduction` section.

1. Connect your keyboard to your computer

2. Launch FL Studio

3. Go to ``Options > MIDI Settings``. You'll find something like this:

   .. image:: ./_resources/installation/script-assignment-1.png

4. Click on the DAW control surface device entries on both Output and Input lists and
   assign them a port. It can be any port you want, but it has to be
   the same on both.

   .. note::
      These ports have nothing to do with the internal/virtual MIDI ports FL Studio uses
      to route MIDI between plugins.

   .. warning::
      **The port number you assign to the keyboard cannot be shared with any other
      MIDI device in the list.** Keep a port for each individual MIDI device you enable
      in FL Studio.

   .. warning::
      **Keep the MIDI keyboard unassigned from any port.** On Windows there's a bug related to
      how MIDI devices are handled and assigning a port to the keyboard will result in an
      "out of memory" error.

      Even if it should only affect to Windows, macOS users are also encouraged to do the same.

   .. image:: ./_resources/installation/script-assignment-2.gif

5. Click on the ``Enable`` button to tell FL Studio to receive MIDI messages from the keyboard.
   Do it both on the MIDI keyboard and the DAW control surface entries.

   .. image:: ./_resources/installation/script-assignment-3.gif

6. Finally, select the DAW device on both Input and Output lists, open the ``Controller type``
   menu and select the ``Native Instruments Komplete Kontrol (user)`` script.

   .. image:: ./_resources/installation/script-assignment-4.gif

**Bonus for S-Series keyboards:** There should be a second MIDI script on the list called "Native Instruments Komplete Kontrol (S-Series Custom MIDI Map) (user)". You can link this script to the MIDI port of your keyboard (named "Komplete Kontrol - X") to use the white buttons at the top of the screen when the keyboard is on MIDI mode to trigger different actions inside FL Studio (you need to be using the default MIDI template from the Komplete Kontrol software in order for this optional script to work):

========= ============================================
  Button   Action                                    
========= ============================================
 1st       Creates a new pattern and asks for a name 
 2nd       Shows the playlist                        
 3rd       Shows the channel rack                    
 4th       Shows the piano roll                      
 5th       Shows the full-screen plugin picker       
 6th       Shows the mixer                           
 7th       Shows the MIDI settings                   
 8th       Closes all windows        
========= ============================================

Updating the script
===================

To update to a newer version of the script, just delete the ``Native Instruments Komplete Kontrol`` folder
from the ``Hardware`` folder and install the new version following these same steps. Re-assigning the script
on the FL Studio MIDI settings shouldn't be necessary as the script paths will be exactly the same.

.. _troubleshooting:

Troubleshooting
===============

- **Powercycle your device:** As simple or stupid it might appear to be, turning your device off and on might solve some problems in certain situations. Try it first before doing anything more if you have any problems:
  
  - **S-Series:** These ones have a dedicated power on/off button on the back. Use it to turn your device off and back on.
  
  - **A-Series and M-Series:** These power on and off only by the USB power. To turn off and on your device, just unplug it from your PC and then plug it back.
  
  - If this does nothing, try restarting your PC as well.

- **There's no DAW MIDI port (more typical on Windows, but might happen on macOS as well):** The DAW port is a virtual MIDI port created by the drivers of the keyboard when they detect a Komplete Keyboard connected. If it doesn't appear then it might be due to a corrupt driver install or an error on the initialization of the driver. Try to reboot your PC. If that doesn't work, then:
  
  - Disconnect any NI device from your PC
  
  - Go to the Windows Settings (or the Control Panel) and uninstall all of the Komplete Kontrol named elements on the Apps and Features list:
    
    .. image:: ./_resources/installation/troubleshooting-1.png
  
  - Restart your computer
  
  - Run Native Access as an administrator and re-install Komplete Kontrol
  
  - Run Komplete Kontrol as an administrator to finalize the installation of the drivers
  
  - If you have an S-Series device, you might need to reinstall the standalone driver as well. You can download it from Native Instrument's `drivers catalog <https://www.native-instruments.com/en/support/downloads/drivers-other-files/>`__
  
  - Restart your PC once again
  
  - If the problem persists, contact Native Instruments to get technical support
