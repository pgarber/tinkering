PULP_HOME=/git/pulp/platform
PULP_RPM_HOME=/git/pulp_rpm

TITO_BUILD_ID=./test_build_num

BUILD_ID=`cat $TITO_BUILD_ID`
echo $((BUILD_ID + 1)) > $TITO_BUILD_ID

TITO_TEST_BUILD_SRPM="tito_mod build --test --srpm --builder-arg=build=$BUILD_ID"
TITO_TEST_BUILD_RPM="tito_mod build --test --rpm --builder-arg=build=$BUILD_ID"


pushd ${PULP_HOME}
$TITO_TEST_BUILD_SRPM
popd
pushd ${PULP_RPM_HOME}
$TITO_TEST_BUILD_SRPM

