Name:           gstreamer-ffmpeg
Version:        0.10.13
Release:        15%{?dist}
Summary:        GStreamer FFmpeg-based plug-ins
Group:          Applications/Multimedia
# the ffmpeg plugin is LGPL, the postproc plugin is GPL
License:        GPLv2+ and LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source0:        http://gstreamer.freedesktop.org/src/gst-ffmpeg/gst-ffmpeg-%{version}.tar.bz2
# We drop in a newer libav to get all the security bugfixes from there!
Source1:        http://libav.org/releases/libav-0.8.17.tar.xz
Patch0:         gst-ffmpeg-0.10.12-ChangeLog-UTF-8.patch
# Patches cherry picked from upstream for newer libav and bugfixes
Patch1:         0001-configure.ac-Fix-for-new-libav.patch
Patch2:         0002-gstffmpegutils-Fix-include.patch
Patch3:         0003-gstffmpegdec-Re-enable-MT-decoding-by-default.patch
Patch4:         0004-ffmpeg-fix-pad-template-ref-leaks.patch
Patch5:         0005-ffmpegdec-Report-latency-if-B-frames-are-present.patch
Patch6:         0006-ffmpeg-Channel-layouts-are-now-set-for-DTS-and-E-AC3.patch
Patch7:         0007-ffmpegdemux-fix-caps-leak.patch
Patch8:         0008-ffdec-Only-set-get_buffer-function-for-video.patch
Patch9:         0009-codecmap-Add-mapping-for-Indeo-4-video-codec.patch
Patch10:        0010-ffmpegdec-Use-auto-threads-if-available-and-only-sli.patch
Patch11:        0011-ffmux-Use-correct-enum-type-for-return-value.patch
Patch12:        0012-ffdec-don-t-flush-buffers-on-DISCONT.patch
BuildRequires:  gstreamer-devel >= 0.10.0
BuildRequires:  gstreamer-plugins-base-devel >= 0.10.0
BuildRequires:  orc-devel bzip2-devel zlib-devel
%ifarch %{ix86} x86_64
BuildRequires:  yasm
%endif

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

This package provides FFmpeg-based GStreamer plug-ins.


%prep
%setup -q -n gst-ffmpeg-%{version} -a 1
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
rm -r gst-libs/ext/libav
mv libav-0.8.17 gst-libs/ext/libav


%build
# Note no --with-system-ffmpeg *for now*, as gst-ffmpeg wants libav-0.8,
# and the system ffmpeg is 0.11, which is more or less libav-0.9
%configure --disable-dependency-tracking --disable-static \
  --with-package-name="gst-plugins-ffmpeg rpmfusion rpm" \
  --with-package-origin="http://rpmfusion.org/" \
  --with-ffmpeg-extra-configure="--enable-runtime-cpudetect --arch=%{_target_cpu} --optflags=\\\"\\\$RPM_OPT_FLAGS\\\""
make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT V=1
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/libgst*.la


%files
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/gstreamer-0.10/libgstffmpeg.so
%{_libdir}/gstreamer-0.10/libgstffmpegscale.so
%{_libdir}/gstreamer-0.10/libgstpostproc.so


%changelog
* Sat May 16 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-15
- Upgrade the buildin libav to 0.8.17 to get all the security fixes from
  upstream libav

* Wed Oct  1 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-14
- Upgrade the buildin libav to 0.8.16 to get all the security fixes from
  upstream libav

* Fri Aug 29 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-13
- Upgrade the buildin libav to 0.8.15 to get all the security fixes from
  upstream libav

* Sun Jun 15 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-12
- Upgrade the buildin libav to 0.8.12 to get all the security fixes from
  upstream libav

* Sun Mar  2 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-11
- Upgrade the buildin libav to 0.8.10 to get all the security fixes from
  upstream libav

* Sat Nov 16 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-10
- Upgrade the buildin libav to 0.8.9 to get all the security fixes from
  upstream libav

* Thu Aug  8 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-9
- Upgrade the buildin libav to 0.8.8 to get all the security fixes from
  upstream libav

* Mon Mar 25 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-8
- Upgrade the buildin libav to 0.8.6 to get all the security fixes from
  upstream libav

* Sun Mar 10 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-7
- Add a patch from upstream libav to fix miscompilation with gcc-4.8
  (rf#2713, libav#388)

* Sat Mar  2 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-6
- Upgrade the buildin libav to 0.8.5 to get all the security fixes from
  upstream libav

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.10.13-5
- Rebuilt for FFmpeg 1.0

* Sun Nov  4 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-4
- Upgrade the buildin libav to 0.8.4 to get all the security fixes from
  upstream libav
- Build included libav with the default RPM_OPT_FLAGS (rf#2560, rf#2472)

* Thu Jul 12 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-3
- Switch to the build in libav for now, gst-ffmpeg wants libav-0.8,
  and the system ffmpeg is 0.11, which is more or less the unreleased
  libav-0.9. Once libav-0.9 gets officially released gst-ffmpeg will
  hopefully switch to it
- Upgrade the buildin libav to 0.8.3 to get all the security fixes from
  upstream libav

* Tue Feb 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.10.13-2
- Rebuilt for x264/FFmpeg

* Sun Jan 29 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.13-1
- New upstream release 0.10.13 (rf#2118, rf#2069)

* Sun Sep  4 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.12-1
- New upstream release 0.10.12
- Rebuild for ffmpeg-0.8

* Thu Apr 21 2011 Hans de Goede <j.w.r.degoede@gmail.com> - 0.10.11-2
- Rebuild for proper package kit magic provides (rhbz#695730, rf#1707)

* Sat Jul 17 2010 Hans de Goede <j.w.r.degoede@gmail.com> 0.10.11-1
- New upstream release 0.10.11

* Tue Jun 22 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.10-2
- Rebuild to get the proper magic gstreamer provides for packagekit (rf1267)

* Sun Mar 14 2010 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.10-1
- New upstream release 0.10.10

* Sat Nov  7 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.9-1
- New upstream release 0.10.9

* Tue Oct 20 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.10.8-2
- rebuilt

* Tue Aug 11 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.8-1
- New upstream release 0.10.8

* Wed Jun 17 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.7-2
- Rebuild for changes in the gstreamer provides script

* Sun Mar 22 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.7-1
- New upstream release 0.10.7

* Wed Dec 17 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.6-1
- New upstream release 0.10.6

* Sun Sep 14 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.5-1
- New upstream release 0.10.5
- Drop all patches, all upstreamed <yeah>

* Thu Jul 24 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.4-2
- Release bump for rpmfusion build

* Thu May 22 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.4-1
- New upstream release 0.10.4
- Drop several upstreamed patches

* Thu May  8 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.3-5
- Fix playback of wvc1 videos (livna bug 1960)

* Thu Apr 10 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.3-4
- Disable ffdec_faad as this has issues (use gstreamer-plugins-bad instead)
  (livna bug 1935)

* Sun Feb 10 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.3-3
- Make gstreamer-ffmpeg work with the new swscaler enabled ffmpeg, this is done
  by disabling the ffvideoscale (FFMPEG Scale) element and another small
  patch (livna bug 1862)

* Tue Feb  5 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.3-2
- Rebuild for new ffmpeg

* Sat Dec 15 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.3-1
- New upstream 0.10.3 release
- Use default RPM_OPT_FLAGS, as we we no longer compile our own ffmpeg
- Drop unneeded libtool BuildRequires

* Mon Nov 12 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-5
- Rebuild for new ffmpeg

* Wed Oct 10 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-4
- Stop gst-inspect --print-all from crashing when we are loaded (reported on
  the mailing list)

* Fri Sep 21 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-3
- Merge freshrpms spec into livna spec for rpmfusion:
- Set release to 3 to be higher as both livna and freshrpms latest release
- Set package name and origin to rpmfusion
- Update license tag for new license tag guidelines
- Build in livna development for testing and for new ffmpeg in livna

* Thu Mar 29 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-2
- Rebuild so that the demuxers get build too (livna bz 1464)

* Fri Jan 19 2007 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-1
- Official upstream 0.10.2 release

* Mon Dec 18 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-0.4.20061108
- Rebuild for new ffmpeg

* Wed Nov 22 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-0.3.20061108
- link libgstpostproc.so with -lpostproc (bug #1288)

* Thu Nov  9 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-0.2.20061108
- Add missing liboil-devel BR

* Wed Nov  8 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.2-0.1.20061108
- New release based on CVS snapshot as upstream hasn't made a new release
  in a while, this fixes bug lvn1235

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.10.1-4
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Sun Sep 24 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.1-3
- Rebuild for FC-6

* Sun Aug 27 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.1-2
- Fix compilation with newer ffmpeg
- drop unnecesarry gcc-c++ BR

* Sun Jul 30 2006 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.1-1
- Minor specfile cleanups for livna submission.
- Add a patch to use the system ffmpeg instead of the included one

* Fri Mar 31 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.1-0.gst.1
- update for new release

* Wed Mar 29 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0.2-0.gst.1
- update for new prerelease

* Fri Mar 17 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.3
- allow "gstreamer" define to be overridden

* Wed Dec 14 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.2
- rebuild against glib 2.8

* Mon Dec 05 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.10.0-0.gst.1
- new release

* Thu Dec 01 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.7-0.gst.1
- new release with 0.10 major/minor

* Sat Nov 12 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.5-0.gst.1
- new upstream release

* Wed Oct 26 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.4-0.gst.1
- new upstream release

* Mon Oct 03 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.9.3-0.gst.1
- new upstream release

* Sat Sep 17 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.6-0.gst.1 new upstream release

* Tue Jun 21 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.5-0.gst.1: for our repo

* Mon Jun 13 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.5-0.lvn.1: new release

* Fri Mar 11 2005 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.4-0.lvn.1: new release

* Fri Dec 31 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.3-0.lvn.1: new release

* Fri Dec 24 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.2.2-0.lvn.1: new prerelease

* Tue Oct 12 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.2-0.lvn.1: new upstream release

* Fri Jul 16 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.1-0.lvn.1: new upstream release

* Fri May 21 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.0-0.lvn.2: update for FC2 and SDL-devel not requiring alsa-lib-devel

* Tue Mar 16 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.0-0.lvn.1: new source release, changed base name to gstreamer

* Fri Mar 05 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.1-0.lvn.2: sync with FreshRPMS

* Tue Mar 02 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.1-0.lvn.1: First package for rpm.livna.org
