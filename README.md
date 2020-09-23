# xcwd-rpm
RPM packaging for [xcwd](https://github.com/schischi/xcwd/).

This is my first attempt at packaging an RPM, so it served as a learning exercice for me.

Here is a little write-up of how I did it.

---

First I searched for documentation online, my first read was https://rpm-packaging-guide.github.io/, highly referenced and maintained by Red Hat officials.

Getting the ropes of it couldn't prove itself hard, I'm used to writing Makefiles and other kind of build system scripts. This is rather similar. A basic RPM spec file goes like this.
```specfile
Name: name-of-the-package
Version: obvious
Release: not so obvious. according to the guide it's "The number of times this version of the software was released"
Summary: very short summary

License: obvious
URL: homepage of the software
Source: Link to the source code of the software

BuildRequires: what is required to build
Requires: what is required to run

%description
A longer description that should not exceed 80 chars by column

%files
The list of files added by this package

%prep
The first step, where the source code is extracted or possibly downloaded and preped, just like the 2 next ones this is written as a script just like dealing with bash

%build
The source code is compiled to binary or equivalent

%install
The binary is installed to the proper directory
```

However, I was missing a few bits, especially about what variables I could use in my file in each sections. Maybe there is a full documentation somewhere, but I couldn't find it. So instead I started looking up for more example. I stumbled across
- https://docs.fedoraproject.org/en-US/quick-docs/creating-rpm-packages/
- https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/Packagers_Guide/chap-Packagers_Guide-Spec_File_Reference-Example.html

Those were a big help, especially the second one near the end when I started tidying up everything.

One of the things that I wanted to achieve was downloading the source code from GitHub. This could pose serious security risks for mitm attacks if no checks are done, but here I do not want to setup an actual build and publishing system. I just wanted to install this piece of software through my package manager instead of compiling it myself and moving it to `/usr/local/bin`, this way I can keep track of what is installed on my computer and uninstall them gracefully. So for me, making my RPM spec file download the source code, or downloading it myself then compiling it would be equivalent, and I wanted to try doing the first one. To achieve this, this SO answer proved useful https://stackoverflow.com/a/48239563. The required information was to use the special command `%undefine _disable_source_fetch` early in my spec file. This allow the rpmbuild tool to download the source code from the provided `Source` meta-tag. I didn't even need to `curl` it myself or anything during one of the build steps! It was done automatically when calling the `%setup` macro during the first step, `%prep`.

Another source of trouble for me was to understand that I did not need to enter into the project source directory before attempting to build or install. Indeed, at the end of the `%prep` step, the source files are downloaded and extracted. So I thought I needed to `cd` into the folder it created before attempting to build it. Turns out a `cd` is automagically done, probably thanks to the `%setup` macro or something.

For the `%build` and `%install` steps, it was rather simple. For the build command I decided to copy it from https://rpm-packaging-guide.github.io/#working-with-spec-files, this "`%{?_smp_mflags}`" stuff probably has a meaning. For the install step, I could not rely on the `%make_install` macro probably because the Makefile from xcwd does not comply to its usage. So instead I translated the example to a simpler form using the `install` command directly, I had to search there and there for what variable names to use, apparently it's `%{buildroot}` and not `%{BUILDROOT}` even though the actual directory is named in all uppercase.

After this, I was still getting a rather annoying error, telling me my "`debugsourcefiles.list`" or something was empty. I have no idea what is its purpose even though I'm guessing it's something related to testing. Since I have no intention to test this software, I quickly searched how to bypass this error. Similarly to the `%undefined _disable_source_fetch` trick, there is a special variable to set to disable the debug steps. I had to add `%global debug_package %{nil}` early in my file for this.

From there I was almost done, `rpmbuild` was still complaining about the `%files` section not being set properly. Indeed I was adding a file at `/usr/bin/xcwd` but not actually telling that this was intended. So I was getting an error that went like "hey, after running everything there is a file left in there, but you never told me you wanted to add a file". Fixing this one was very simple. In the `%files` section I have to add a list of the files that will be installed on the system.

And voilà, running `fedpkg --release f32 local` on my Fedora 32 system effectively created the rpm source and binary packages in my current folder, and I was able to install it using `dnf`.

This was a rather fun and interesting experience, I don't know if I will write more packages or start running copr repositories on my own later, but even if I don't I'm glad I took the effort to gain this extra knowledge. I hope this little reading helped you learning a few things too! You can maybe learn a few more things on my actual blog at https://tina.moe/blog.
