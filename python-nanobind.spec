# See https://docs.fedoraproject.org/en-US/packaging-guidelines/#_compiler_macros
%global toolchain clang

%global nanobind_giturl https://github.com/wjakob/nanobind
%global nanobind_src_dir nanobind-%{version}

Name:           python-nanobind
Version:        2.4.0
Release:        2
Summary:        Tiny and efficient C++/Python bindings

License:        BSD-3-Clause AND MIT
URL:            https://nanobind.readthedocs.org/
VCS:            git:%{nanobind_giturl}.git
Source0:        %{nanobind_giturl}/archive/v%{version}/%{name}-%{version}.tar.gz

# See https://github.com/wjakob/nanobind/pull/815
Patch100:       0001-Properly-install-tsl-robin_map-s-interface-sources.patch
Patch101:       0001-Revert-chore-use-scikit-build-core-0.10-and-auto-min.patch

# TODO(kkleine): This patch is only needed because %%pyproject_wheel
#                calls cmake and I haven't found out how to set
#                NB_USE_SUBMODULE_DEPS=OFF for this call.
Patch102:       0001-Disable-NB_USE_SUBMODULE_DEPS-by-default.patch

BuildArch:      noarch

BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  eigen3-devel
BuildRequires:  librsvg2
BuildRequires:  ninja-build
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  robin-map-devel >= 1.3.0

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
%patch -p1 -P100
%patch -p1 -P101
%patch -p1 -P102
cd ..


%generate_buildrequires
%pyproject_buildrequires


%build
%cmake \
    -G Ninja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{python3_sitelib} \
    -DNB_CREATE_INSTALL_RULES=OFF \
    -DNB_TEST_SANITIZERS_ASAN=OFF \
    -DNB_TEST_SANITIZERS_TSAN=OFF \
    -DNB_TEST_SANITIZERS_UBSAN=OFF \
    -DNB_TEST_SHARED_BUILD=ON \
    -DNB_TEST_STABLE_ABI=OFF
%cmake_build
%pyproject_wheel


%install
#%%cmake_install
%pyproject_install
# Remove not needed files
rm %{buildroot}%{python3_sitelib}/nanobind/cmake/darwin-ld-cpython.sym
rm %{buildroot}%{python3_sitelib}/nanobind/cmake/darwin-ld-pypy.sym
%{__mkdir_p} -v %{buildroot}%{python3_sitelib}/nanobind


%check
%_pyproject_check_import_allow_no_modules -t
pushd %{__cmake_builddir}
%pytest
popd


%files -n python%{python3_pkgversion}-nanobind
%license LICENSE
%dir %{python3_sitelib}/nanobind
%dir %{python3_sitelib}/nanobind/__pycache__
%dir %{python3_sitelib}/nanobind-%{version}.dist-info
%dir %{python3_sitelib}/nanobind-%{version}.dist-info/licenses
%{python3_sitelib}/nanobind-%{version}.dist-info/INSTALLER
%{python3_sitelib}/nanobind-%{version}.dist-info/METADATA
%{python3_sitelib}/nanobind-%{version}.dist-info/WHEEL
%{python3_sitelib}/nanobind-%{version}.dist-info/licenses/LICENSE
%{python3_sitelib}/nanobind/__init__.py
%{python3_sitelib}/nanobind/__main__.py
%{python3_sitelib}/nanobind/__pycache__/__init__.*.pyc
%{python3_sitelib}/nanobind/__pycache__/__main__.*.pyc
%{python3_sitelib}/nanobind/__pycache__/stubgen.*.pyc


%files -n python%{python3_pkgversion}-nanobind-devel
%license LICENSE
%dir %{python3_sitelib}/nanobind/include
%dir %{python3_sitelib}/nanobind/include/nanobind
%dir %{python3_sitelib}/nanobind/include/nanobind/eigen
%dir %{python3_sitelib}/nanobind/include/nanobind/intrusive
%dir %{python3_sitelib}/nanobind/include/nanobind/stl
%dir %{python3_sitelib}/nanobind/include/nanobind/stl/detail
%dir %{python3_sitelib}/nanobind/src
%dir %{python3_sitelib}/nanobind/cmake
%{python3_sitelib}/nanobind/cmake/nanobind-config-version.cmake
%{python3_sitelib}/nanobind/cmake/nanobind-config.cmake
%{python3_sitelib}/nanobind/include/nanobind/eigen/dense.h
%{python3_sitelib}/nanobind/include/nanobind/eigen/sparse.h
%{python3_sitelib}/nanobind/include/nanobind/eval.h
%{python3_sitelib}/nanobind/include/nanobind/intrusive/counter.h
%{python3_sitelib}/nanobind/include/nanobind/intrusive/counter.inl
%{python3_sitelib}/nanobind/include/nanobind/intrusive/ref.h
%{python3_sitelib}/nanobind/include/nanobind/make_iterator.h
%{python3_sitelib}/nanobind/include/nanobind/nanobind.h
%{python3_sitelib}/nanobind/include/nanobind/nb_accessor.h
%{python3_sitelib}/nanobind/include/nanobind/nb_attr.h
%{python3_sitelib}/nanobind/include/nanobind/nb_call.h
%{python3_sitelib}/nanobind/include/nanobind/nb_cast.h
%{python3_sitelib}/nanobind/include/nanobind/nb_class.h
%{python3_sitelib}/nanobind/include/nanobind/nb_defs.h
%{python3_sitelib}/nanobind/include/nanobind/nb_descr.h
%{python3_sitelib}/nanobind/include/nanobind/nb_enums.h
%{python3_sitelib}/nanobind/include/nanobind/nb_error.h
%{python3_sitelib}/nanobind/include/nanobind/nb_func.h
%{python3_sitelib}/nanobind/include/nanobind/nb_lib.h
%{python3_sitelib}/nanobind/include/nanobind/nb_misc.h
%{python3_sitelib}/nanobind/include/nanobind/nb_python.h
%{python3_sitelib}/nanobind/include/nanobind/nb_traits.h
%{python3_sitelib}/nanobind/include/nanobind/nb_tuple.h
%{python3_sitelib}/nanobind/include/nanobind/nb_types.h
%{python3_sitelib}/nanobind/include/nanobind/ndarray.h
%{python3_sitelib}/nanobind/include/nanobind/operators.h
%{python3_sitelib}/nanobind/include/nanobind/stl/array.h
%{python3_sitelib}/nanobind/include/nanobind/stl/bind_map.h
%{python3_sitelib}/nanobind/include/nanobind/stl/bind_vector.h
%{python3_sitelib}/nanobind/include/nanobind/stl/chrono.h
%{python3_sitelib}/nanobind/include/nanobind/stl/complex.h
%{python3_sitelib}/nanobind/include/nanobind/stl/detail/chrono.h
%{python3_sitelib}/nanobind/include/nanobind/stl/detail/nb_array.h
%{python3_sitelib}/nanobind/include/nanobind/stl/detail/nb_dict.h
%{python3_sitelib}/nanobind/include/nanobind/stl/detail/nb_list.h
%{python3_sitelib}/nanobind/include/nanobind/stl/detail/nb_optional.h
%{python3_sitelib}/nanobind/include/nanobind/stl/detail/nb_set.h
%{python3_sitelib}/nanobind/include/nanobind/stl/detail/traits.h
%{python3_sitelib}/nanobind/include/nanobind/stl/filesystem.h
%{python3_sitelib}/nanobind/include/nanobind/stl/function.h
%{python3_sitelib}/nanobind/include/nanobind/stl/list.h
%{python3_sitelib}/nanobind/include/nanobind/stl/map.h
%{python3_sitelib}/nanobind/include/nanobind/stl/optional.h
%{python3_sitelib}/nanobind/include/nanobind/stl/pair.h
%{python3_sitelib}/nanobind/include/nanobind/stl/set.h
%{python3_sitelib}/nanobind/include/nanobind/stl/shared_ptr.h
%{python3_sitelib}/nanobind/include/nanobind/stl/string_view.h
%{python3_sitelib}/nanobind/include/nanobind/stl/string.h
%{python3_sitelib}/nanobind/include/nanobind/stl/tuple.h
%{python3_sitelib}/nanobind/include/nanobind/stl/unique_ptr.h
%{python3_sitelib}/nanobind/include/nanobind/stl/unordered_map.h
%{python3_sitelib}/nanobind/include/nanobind/stl/unordered_set.h
%{python3_sitelib}/nanobind/include/nanobind/stl/variant.h
%{python3_sitelib}/nanobind/include/nanobind/stl/vector.h
%{python3_sitelib}/nanobind/include/nanobind/stl/wstring.h
%{python3_sitelib}/nanobind/include/nanobind/trampoline.h
%{python3_sitelib}/nanobind/include/nanobind/typing.h
%{python3_sitelib}/nanobind/src/buffer.h
%{python3_sitelib}/nanobind/src/common.cpp
%{python3_sitelib}/nanobind/src/error.cpp
%{python3_sitelib}/nanobind/src/hash.h
%{python3_sitelib}/nanobind/src/implicit.cpp
%{python3_sitelib}/nanobind/src/nb_combined.cpp
%{python3_sitelib}/nanobind/src/nb_enum.cpp
%{python3_sitelib}/nanobind/src/nb_func.cpp
%{python3_sitelib}/nanobind/src/nb_internals.cpp
%{python3_sitelib}/nanobind/src/nb_internals.h
%{python3_sitelib}/nanobind/src/nb_ndarray.cpp
%{python3_sitelib}/nanobind/src/nb_static_property.cpp
%{python3_sitelib}/nanobind/src/nb_type.cpp
%{python3_sitelib}/nanobind/src/trampoline.cpp
%{python3_sitelib}/nanobind/stubgen.py


%changelog
* Fri Dec 13 2024 Konrad Kleine <kkleine@redhat.com> - 2.4.0-2
- Do not vendor robin-map but use system package robin-map-devel

* Fri Dec 13 2024 Konrad Kleine <kkleine@redhat.com> - 2.4.0-1
- First release of python-nanobind
