# See https://docs.fedoraproject.org/en-US/packaging-guidelines/#_compiler_macros
%global toolchain clang

%global giturl https://github.com/wjakob/nanobind

Name:           python-nanobind
Version:        2.4.0
Release:        %autorelease
Summary:        Tiny and efficient C++/Python bindings

License:        BSD-3-Clause AND MIT
URL:            https://nanobind.readthedocs.org/
VCS:            git:%{giturl}.git
Source0:        %{giturl}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  clang
BuildRequires:  cmake
BuildRequires:  eigen3-devel
BuildRequires:  librsvg2
BuildRequires:  ninja-build
BuildRequires:  robin-map-devel >= 1.3.0
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-furo
BuildRequires:  python%{python3_pkgversion}-numpy
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-scipy
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinx-copybutton
BuildRequires:  python%{python3_pkgversion}-sphinxcontrib-svg2pdfconverter-common

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
Requires:       %{name} = %{version}-%{release}
Requires:       python%{python3_pkgversion}-nanobind-robin-map-devel = %{version}-%{release}
Requires:       python3-scikit-build-core
%description -n python%{python3_pkgversion}-nanobind-devel
Development files for nanobind.


%package -n     python%{python3_pkgversion}-nanobind-robin-map-devel
Summary:        C++ implementation of a fast hash map and hash set using robin hood hashing
License:        MIT
Requires:       %{name} = %{version}-%{release}
Requires:       robin-map-devel >= 1.3.0
%description -n python%{python3_pkgversion}-nanobind-robin-map-devel
The robin-map library is a C++ implementation of a fast hash
map and hash set using open-addressing and linear robin hood
hashing with backward shift deletion to resolve collisions.

%prep
%autosetup -p1 -n nanobind-%{version}

# Fake existence of ext/robin_map/include to fool naonbind build
# NOTE: You have to have robin-map-devel installed.
rm -rfv ext
%{__mkdir_p} -v ext/robin_map/include/tsl
ln -svf %{_includedir}/tsl/robin_*.h ext/robin_map/include/tsl
ln -svf %{_datadir}/licenses/robin-map-devel ext/robin_map/LICENSE


%generate_buildrequires
%pyproject_buildrequires


%build
%cmake \
    -G Ninja \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{python3_sitelib} \
    -Dtsl-robin-map_DIR=%{_datadir}/cmake/tsl-robin-map/ \
    -DNB_CREATE_INSTALL_RULES=OFF \
    -DNB_USE_SUBMODULE_DEPS=OFF \
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

# Remove the files that we already ship in robin-map-devel and
# create symbolic links instead. We need to maintain the directory
# structure because it is hard-coded in nanobind.
%{__mkdir_p} -v %{buildroot}%{python3_sitelib}/nanobind/ext/robin_map/include/tsl
pushd %{buildroot}%{python3_sitelib}/nanobind/ext/robin_map/include/tsl
ln -svf ../../../../../../../../include/tsl/robin_growth_policy.h .
ln -svf ../../../../../../../../include/tsl/robin_hash.h .
ln -svf ../../../../../../../../include/tsl/robin_map.h .
ln -svf ../../../../../../../../include/tsl/robin_set.h .
popd

install %{_datadir}/licenses/robin-map-devel/LICENSE %{buildroot}%{python3_sitelib}/nanobind/ext/robin_map/LICENSE

%{__mkdir_p} -v %{buildroot}%{python3_sitelib}/nanobind
install -m 0755 src/stubgen.py %{buildroot}%{python3_sitelib}/nanobind/stubgen.py


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


%files -n python%{python3_pkgversion}-nanobind-robin-map-devel
%license %{python3_sitelib}/nanobind/ext/robin_map/LICENSE
%dir %{python3_sitelib}/nanobind/ext
%dir %{python3_sitelib}/nanobind/ext/robin_map
%dir %{python3_sitelib}/nanobind/ext/robin_map/include
%dir %{python3_sitelib}/nanobind/ext/robin_map/include/tsl
%{python3_sitelib}/nanobind/ext/robin_map/include/tsl/*.h


%changelog
%autochangelog