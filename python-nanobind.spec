# See https://docs.fedoraproject.org/en-US/packaging-guidelines/#_compiler_macros
%global toolchain clang

%global nanobind_giturl https://github.com/wjakob/nanobind
%global nanobind_src_dir nanobind-%{version}

Name:           python-nanobind
Version:        2.4.0
Release:        5%{?dist}
Summary:        Tiny and efficient C++/Python bindings

License:        BSD-3-Clause
URL:            https://nanobind.readthedocs.org/
VCS:            git:%{nanobind_giturl}.git
Source0:        %{nanobind_giturl}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  eigen3-devel
BuildRequires:  librsvg2
BuildRequires:  ninja-build
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  robin-map-devel >= 1.3.0

Requires:  robin-map-devel >= 1.3.0

%global _description %{expand:
nanobind is a small binding library that exposes C++ types
in Python and vice versa. It is reminiscent of Boost.Python
and pybind11 and uses near-identical syntax.
In contrast to these existing tools, nanobind is more
efficient: bindings compile in a shorter amount of time,
produce smaller binaries, and have better runtime performance.}

%description %_description

%package -n     python%{python3_pkgversion}-nanobind
Summary:        %{summary}
License:        BSD-3-Clause
%description -n python%{python3_pkgversion}-nanobind %_description


%package -n     python%{python3_pkgversion}-nanobind-devel
Summary:        Development files for nanobind
License:        BSD-3-Clause
Requires:       python%{python3_pkgversion}-nanobind = %{version}-%{release}
%description -n python%{python3_pkgversion}-nanobind-devel
Development files for nanobind.


%prep
%autosetup -N -T -b 0 -n %{nanobind_src_dir}


%generate_buildrequires
%pyproject_buildrequires


%build
# See https://github.com/scikit-build/scikit-build-core?tab=readme-ov-file#configuration
%{pyproject_wheel: \
-C"build-dir=%{__cmake_builddir}" \
-C"cmake.define.NB_USE_SUBMODULE_DEPS=false" \
-C"cmake.build-type=RelWithDebInfo" \
-C"cmake.define.NB_TEST_SHARED_BUILD=false" \
-C"cmake.define.NB_TEST=true" \
-C"build.verbose=true" \
}

%install
%pyproject_install
%pyproject_save_files -L nanobind


%check
%pyproject_check_import
# Test files are not installed, hence we need
# to enter the build directory manually.
pushd %{__cmake_builddir}
%pytest
popd


%files -n python%{python3_pkgversion}-nanobind -f %{pyproject_files}
%license %{python3_sitelib}/nanobind-%{version}.dist-info/licenses/LICENSE
%exclude %{python3_sitelib}/nanobind/include
%exclude %{python3_sitelib}/nanobind/src
%exclude %{python3_sitelib}/nanobind/cmake
%pycached %exclude %{python3_sitelib}/nanobind/stubgen.py
# Exclude not needed files
%exclude %{python3_sitelib}/nanobind/cmake/darwin-ld-cpython.sym
%exclude %{python3_sitelib}/nanobind/cmake/darwin-ld-pypy.sym


%files -n python%{python3_pkgversion}-nanobind-devel
%{python3_sitelib}/nanobind/include/
%{python3_sitelib}/nanobind/src/
%{python3_sitelib}/nanobind/cmake/
%pycached %{python3_sitelib}/nanobind/stubgen.py


%changelog
* Fri Dec 13 2024 Konrad Kleine <kkleine@redhat.com> - 2.4.0-5
- Better license and files section handling

* Fri Dec 13 2024 Konrad Kleine <kkleine@redhat.com> - 2.4.0-4
- No more manual cmake invocation and proper use of %%pyproject_save_files

* Fri Dec 13 2024 Konrad Kleine <kkleine@redhat.com> - 2.4.0-3
- License and patch cleanup

* Fri Dec 13 2024 Konrad Kleine <kkleine@redhat.com> - 2.4.0-2
- Do not vendor robin-map but use system package robin-map-devel

* Fri Dec 13 2024 Konrad Kleine <kkleine@redhat.com> - 2.4.0-1
- First release of python-nanobind
