Name:           gstreamer-ffmpeg
Version:        0.10.4
Release:        2%{?dist}.1
Summary:        GStreamer FFmpeg-based plug-ins
Group:          Applications/Multimedia
# the ffmpeg plugin is LGPL, the postproc plugin is GPL
License:        GPLv2+ and LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source:         http://gstreamer.freedesktop.org/src/gst-ffmpeg/gst-ffmpeg-%{version}.tar.bz2
# submitted upstream: http://bugzilla.gnome.org/show_bug.cgi?id=534392
Patch1:         gst-ffmpeg-0.10.3-no-ffdec_faad.patch
# submitted upstream: http://bugzilla.gnome.org/show_bug.cgi?id=534390
Patch2:         gst-ffmpeg-0.10.4-av_picture_copy.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  gstreamer-devel >= 0.10.0
BuildRequires:  gstreamer-plugins-base-devel >= 0.10.0
BuildRequires:  ffmpeg-devel liboil-devel

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new 
plugins.

This package provides FFmpeg-based GStreamer plug-ins.


%prep
%setup -q -n gst-ffmpeg-%{version}
%patch1 -p1
%patch2 -p1
# adjust includes for the header move in latest ffmpeg <sigh>
sed -i -e 's|ffmpeg/avcodec.h|ffmpeg/libavcodec/avcodec.h|g' \
  -e 's|ffmpeg/avformat.h|ffmpeg/libavformat/avformat.h|g' \
  -e 's|postproc/postprocess.h|ffmpeg/libpostproc/postprocess.h|g' \
  -e 's|ffmpeg/swscale.h|ffmpeg/libswscale/swscale.h|g' \
  ext/ffmpeg/*.c ext/ffmpeg/*.h ext/libpostproc/*.c


%build
%configure --disable-dependency-tracking --disable-static \
  --with-package-name="gst-plugins-ffmpeg rpmfusion rpm" \
  --with-package-origin="http://rpmfusion.org/" \
  --with-system-ffmpeg
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-0.10/libgst*.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_libdir}/gstreamer-0.10/libgstffmpeg.so
%{_libdir}/gstreamer-0.10/libgstpostproc.so


%changelog
* Sat Aug 16 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.10.4-2.fc9.1
- Fix build with new ffmpeg

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
