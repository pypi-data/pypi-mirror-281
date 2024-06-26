Main methods
============

.. _api_signal:

Signal methods
--------------

.. tabs::

    .. group-tab:: GPU version

        .. autofunction:: ultraspy.down_mix

        .. autofunction:: ultraspy.filtfilt

        .. autofunction:: ultraspy.rf2iq

        .. autofunction:: ultraspy.matched_filter

        .. autofunction:: ultraspy.normalize

    .. group-tab:: CPU version

        .. autofunction:: ultraspy.cpu.down_mix

        .. autofunction:: ultraspy.cpu.filtfilt

        .. autofunction:: ultraspy.cpu.rf2iq

        .. autofunction:: ultraspy.cpu.matched_filter

        .. autofunction:: ultraspy.cpu.normalize


.. _api_doppler:

Doppler methods
---------------

.. tabs::

    .. group-tab:: GPU version

        .. autofunction:: ultraspy.apply_wall_filter

        .. autofunction:: ultraspy.spatial_smoothing

        .. autofunction:: ultraspy.get_color_doppler_map

        .. autofunction:: ultraspy.get_power_doppler_map

        .. autofunction:: ultraspy.gpu.doppler.dual_frequency_unalias

    .. group-tab:: CPU version

        .. autofunction:: ultraspy.cpu.apply_wall_filter

        .. autofunction:: ultraspy.cpu.spatial_smoothing

        .. autofunction:: ultraspy.cpu.get_color_doppler_map

        .. autofunction:: ultraspy.cpu.get_power_doppler_map

        .. autofunction:: ultraspy.cpu.doppler.dual_frequency_unalias


.. _api_display:

Display methods
---------------

.. tabs::

    .. group-tab:: GPU version

        .. autofunction:: ultraspy.to_b_mode

        .. autofunction:: ultraspy.get_spectrum

        .. autofunction:: ultraspy.get_doppler_colormap

    .. group-tab:: CPU version

        .. autofunction:: ultraspy.cpu.to_b_mode

        .. autofunction:: ultraspy.cpu.get_spectrum


.. _api_postpro:

Post-processing methods
-----------------------

.. tabs::

    .. group-tab:: GPU version

        .. autofunction:: ultraspy.distort_dynamic

    .. group-tab:: CPU version

        .. autofunction:: ultraspy.cpu.distort_dynamic
