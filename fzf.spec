# TODO:
# - package vendored modules
# - package fzf-tmux

%define		fzfrev		19759ed
%define		fzfvimrev	711fb41
%define		vendor_version	0.27.0

Summary:	A command-line fuzzy finder written in Go
Name:		fzf
Version:	0.27.0
Release:	1
License:	MIT
Group:		Applications/Shells
#Source0Download: https://github.com/junegunn/fzf/releases
Source0:	https://github.com/junegunn/fzf/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	498b121f93733e45b4c432c3549b68f8
# cd fzf-%{version}
# go mod vendor
# cd ..
# tar cJf fzf-vendor-%{version}.tar.xz fzf-%{version}/vendor
Source1:	%{name}-vendor-%{vendor_version}.tar.xz
# Source1-md5:	8f6ede1f36704a492d45b534c18a0124
Source2:	https://github.com/junegunn/fzf.vim/archive/%{fzfvimrev}/fzf.vim-%{fzfvimrev}.tar.gz
# Source2-md5:	1a4ec38922f1a9b0483d2c7b4a1cc1a9
URL:		https://github.com/junegunn/fzf
BuildRequires:	golang >= 1.13
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
ExclusiveArch:	%{ix86} %{x8664} %{arm} aarch64 mips64 mips64le ppc64 ppc64le s390x
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
BuildArch:	noarch

%description -n bash-completion-fzf
bash-completion for fzf.

%package -n zsh-completion-fzf
Summary:	zsh-completion for fzf
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

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
BuildArch:	noarch

%description -n vim-plugin-fzf
fzf integration for Vim.

%package -n vim-plugin-fzf-doc
Summary:	Documentation for fzf Vim plugin
Group:		Applications/Editors/Vim
Requires:	vim-plugin-fzf = %{version}-%{release}
Requires:	vim-rt
BuildArch:	noarch

%description -n vim-plugin-fzf-doc
Documentation for fzf Vim plugin.

%prep
%setup -q -a1 -a2
%{__mv} fzf-%{vendor_version}/vendor .
%{__mv} fzf.vim-%{fzfvimrev}* fzf.vim
%{__sed} -i -e "s@let s:bin_dir = .*@let s:bin_dir = '%{_datadir}/fzf/vim/bin/'@" fzf.vim/autoload/fzf/vim.vim
%{__sed} -i -e '1s,.*env bash,#!/bin/bash,' fzf.vim/bin/preview.sh
%{__sed} -i -e '1s,.*env perl,#!%{__perl},' fzf.vim/bin/tags.pl

%{__mkdir_p} .go-cache

%build
GOCACHE="$(pwd)/.go-cache" go build -v -mod=vendor -ldflags='-X main.version=%{version} -X main.revision=%{fzfrev}' -o target/fzf

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/fzf/vim/bin,%{_mandir}/man1,%{bash_compdir},%{zsh_compdir}}
install -d $RPM_BUILD_ROOT%{_datadir}/vim/{doc,autoload,plugin/fzf}

cp -p target/fzf $RPM_BUILD_ROOT%{_bindir}/fzf
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
