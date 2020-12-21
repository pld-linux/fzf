# TODO:
# - package vendored modules
# - package fzf-tmux

%define		fzfrev		 e3e76fa
%define		fzfvimrev	 8fa9cf0

Summary:	A command-line fuzzy finder written in Go
Name:		fzf
Version:	0.24.4
Release:	1
License:	MIT
Group:		Applications/Shells
#Source0Download: https://github.com/junegunn/fzf/releases
Source0:	https://github.com/junegunn/fzf/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	e627828780d41ded82cb9209642ce985
# cd fzf-%{version}
# go mod vendor
# cd ..
# tar cJf fzf-vendor-%{version}.tar.xz fzf-%{version}/vendor
Source1:	%{name}-vendor-%{version}.tar.xz
# Source1-md5:	64f38dfc6f0cd4fc0008c45096223116
Source2:	https://github.com/junegunn/fzf.vim/archive/%{fzfvimrev}/fzf.vim-%{fzfvimrev}.tar.gz
# Source2-md5:	4d299b3212e34c57f966ec8f7562525d
URL:		https://github.com/junegunn/fzf
BuildRequires:	golang >= 1.13
BuildRequires:	sed >= 4.0
ExclusiveArch:	%{x8664} armv5l armv5tel armv5tejl armv6l armv6hl armv7l armv7hl armv7hnl armv8l armv8hll armv8hnl armv8hcnl aarch64 ppc64le
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
fzf is a general-purpose command-line fuzzy finder.

It's an interactive Unix filter for command-line that can be used with
any list; files, command history, processes, hostnames, bookmarks, git
commits, etc.

%package -n bash-completion-fzf
Summary:	bash-completion for fzf
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description -n bash-completion-fzf
bash-completion for fzf.

%package -n zsh-completion-fzf
Summary:	zsh-completion for fzf
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description -n zsh-completion-fzf
zsh-completion for fzf.

%package -n vim-plugin-fzf
Summary:	fzf integration for Vim
Group:		Applications/Editors/Vim
Requires:	%{name} >= 0.23.0
Requires:	file
Requires:	vim-rt
Suggests:	highlight
Suggests:	the_silver_searcher
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description -n vim-plugin-fzf
fzf integration for Vim.

%package -n vim-plugin-fzf-doc
Summary:	Documentation for fzf Vim plugin
Group:		Applications/Editors/Vim
Requires:	vim-plugin-fzf = %{version}-%{release}
Requires:	vim-rt
%if "%{_rpmversion}" >= "4.6"
BuildArch:	noarch
%endif

%description -n vim-plugin-fzf-doc
Documentation for fzf Vim plugin.

%prep
%setup -q -b1 -a2
%{__mv} fzf.vim-%{fzfvimrev}* fzf.vim
%{__sed} -i -e "s@let s:bin_dir = .*@let s:bin_dir = '%{_datadir}/fzf/vim/bin/'@" fzf.vim/autoload/fzf/vim.vim
%{__sed} -i -e '1s,.*env bash,#!/bin/bash,' fzf.vim/bin/preview.sh
%{__sed} -i -e '1s,.*env perl,#!%{__perl},' fzf.vim/bin/tags.pl

%build
%{__make} \
%ifarch armv5tl armv5tel arm5tejl
	UNAME_M=armv5l \
%else
%ifarch armv6l armv6hl
	UNAME_M=armv6l \
%else
%ifarch armv7l armv7hl armv7hnl
	UNAME_M=armv6l \
%else
%ifarch armv8l armv8hl armv8hnl armv8hcnl
	UNAME_M=armv8l \
%else
	UNAME_M=%{_target_cpu} \
%endif
%endif
%endif
%endif
	FZF_VERSION=%{version} FZF_REVISION=%{fzfrev} GOFLAGS=-mod=vendor

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/fzf/vim/bin,%{_mandir}/man1,%{bash_compdir},%{zsh_compdir}}
install -d $RPM_BUILD_ROOT%{_datadir}/vim/{doc,autoload,plugin/fzf}

cp -p target/fzf-linux* $RPM_BUILD_ROOT%{_bindir}/fzf
cp -p man/man1/fzf.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p shell/completion.bash $RPM_BUILD_ROOT%{_datadir}/fzf
cp -p shell/key-bindings.bash $RPM_BUILD_ROOT%{_datadir}/fzf
cp -p shell/completion.zsh $RPM_BUILD_ROOT%{_datadir}/fzf
cp -p shell/key-bindings.zsh $RPM_BUILD_ROOT%{_datadir}/fzf
cp -rp fzf.vim/autoload/fzf $RPM_BUILD_ROOT%{_datadir}/vim/autoload
cp -p plugin/fzf.vim $RPM_BUILD_ROOT%{_datadir}/vim/plugin/fzf.vim
cp -p fzf.vim/plugin/fzf.vim $RPM_BUILD_ROOT%{_datadir}/vim/plugin/fzf/fzf.vim
cp -p fzf.vim/doc/fzf-vim.txt $RPM_BUILD_ROOT%{_datadir}/vim/doc/fzf.txt
cp -p fzf.vim/bin/{preview.sh,tags.pl} $RPM_BUILD_ROOT%{_datadir}/fzf/vim/bin

%clean
rm -rf $RPM_BUILD_ROOT

%post -n vim-plugin-fzf-doc
%vim_doc_helptags

%postun -n vim-plugin-fzf-doc
%vim_doc_helptags

%files
%defattr(644,root,root,755)
%doc BUILD.md CHANGELOG.md README.md
%attr(755,root,root) %{_bindir}/fzf
%dir %{_datadir}/fzf
%{_mandir}/man1/fzf.1*

%files -n bash-completion-fzf
%defattr(644,root,root,755)
%{_datadir}/fzf/completion.bash
%{_datadir}/fzf/key-bindings.bash

%files -n zsh-completion-fzf
%defattr(644,root,root,755)
%{_datadir}/fzf/completion.zsh
%{_datadir}/fzf/key-bindings.zsh

%files -n vim-plugin-fzf
%defattr(644,root,root,755)
%doc README-VIM.md fzf.vim/README.md
%dir %{_datadir}/fzf/vim
%dir %{_datadir}/fzf/vim/bin
%attr(755,root,root) %{_datadir}/fzf/vim/bin/preview.sh
%attr(755,root,root) %{_datadir}/fzf/vim/bin/tags.pl
%{_datadir}/vim/autoload/fzf
%{_datadir}/vim/plugin/fzf.vim
%{_datadir}/vim/plugin/fzf

%files -n vim-plugin-fzf-doc
%defattr(644,root,root,755)
%{_datadir}/vim/doc/fzf.txt
