# TODO:
# - package vendored modules
# - package fzf-tmux
Summary:	A command-line fuzzy finder written in Go
Name:		fzf
Version:	0.21.1
Release:	1
License:	MIT
Group:		Applications/Shells
#Source0Download: https://github.com/junegunn/fzf/releases
Source0:	https://github.com/junegunn/fzf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	6c27760987032a0cf847caf61f8e7722
# cd fzf-%{version}
# go mod vendor
# cd ..
# tar cJf fzf-vendor-%{version}.tar.xz fzf-%{version}/vendor
Source1:	%{name}-vendor-%{version}.tar.xz
# Source1-md5:	9ac6ea822f43566753e072fba53b510c
URL:		https://github.com/junegunn/fzf
BuildRequires:	golang >= 1.13
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
Requires:	%{name} = %{version}-%{release}
Requires:	vim-rt
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
%setup -q -b1

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/fzf,%{_mandir}/man1,%{bash_compdir},%{zsh_compdir}}
install -d $RPM_BUILD_ROOT%{_datadir}/vim/{doc,vimfiles/plugin}

cp -p target/fzf-linux* $RPM_BUILD_ROOT%{_bindir}/fzf
cp -p man/man1/fzf.1 $RPM_BUILD_ROOT%{_mandir}/man1
cp -p shell/completion.bash $RPM_BUILD_ROOT%{bash_compdir}/fzf
cp -p shell/key-bindings.bash $RPM_BUILD_ROOT%{_datadir}/fzf
cp -p shell/completion.zsh $RPM_BUILD_ROOT%{zsh_compdir}/_fzf
cp -p shell/key-bindings.zsh $RPM_BUILD_ROOT%{_datadir}/fzf
cp -p plugin/fzf.vim $RPM_BUILD_ROOT%{_datadir}/vim/vimfiles/plugin/fzf.vim
cp -p doc/fzf.txt $RPM_BUILD_ROOT%{_datadir}/vim/doc/fzf.txt

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
%{bash_compdir}/fzf
%{_datadir}/fzf/key-bindings.bash

%files -n zsh-completion-fzf
%defattr(644,root,root,755)
%{zsh_compdir}/_fzf
%{_datadir}/fzf/key-bindings.zsh

%files -n vim-plugin-fzf
%defattr(644,root,root,755)
%doc README-VIM.md
%defattr(644,root,root,755)
%{_datadir}/vim/vimfiles/plugin

%files -n vim-plugin-fzf-doc
%defattr(644,root,root,755)
%{_datadir}/vim/doc/fzf.txt
