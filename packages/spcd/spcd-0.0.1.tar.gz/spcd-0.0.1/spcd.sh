#! /usr/bin/env sh

# defaults
[ -n "${SPCD_DNS}" ] || SPCD_DNS="\
9.9.9.9 \
"
[ -n "${SPCD_GIT_MAIN}" ] || SPCD_GIT_MAIN="spcd"
[ -n "${SPCD_GIT_ROOT}" ] || SPCD_GIT_ROOT="rwx"

# main
spcd_main() {
	spcd_list_environment_variables
	spcd_list_working_directory
	#
	spcd_set_environment_variables
	spcd_set_packages_repositories
	spcd_set_packages_configuration
	#
	spcd_set_https_verification_off
	spcd_set_dns_resolving
	spcd_update_packages_catalog
	spcd_install_packages_tools
	spcd_install_ca_certificates
	spcd_write_ca_certificates
	spcd_update_ca_certificates
	spcd_set_https_verification_on
	spcd_update_packages_catalog
	spcd_upgrade_packages
	spcd_install_git
	spcd_install_python
	# TODO move to Python
	spcd_install_rsync
	# TODO move to Python
	spcd_install_ssh
	spcd_clean_packages_cache
	spcd_install_python_modules
	spcd_write_python_module
	spcd_switch_to_python "${@}"
}

# context

spcd_list_environment_variables() {
	spcd_step "List environment variables"
	for spcd_lev__name in $(printenv | cut -d = -f 1 | sort); do
		spcd_lev__text=""
		eval "spcd_lev__text=\"\${${spcd_lev__name}}\""
		echo "${spcd_lev__name}=${spcd_lev__text}"
	done
}

spcd_list_working_directory() {
	spcd_step "List working directory"
	spcd_lwd__path="$(realpath .)"
	spcd_ls "${spcd_lwd__path}"
}

# steps

spcd_set_environment_variables() {
	spcd_step "Set environment variables"
	# set path
	SPCD_PATH="$(realpath "${0}")"
	spcd_echo "SPCD_PATH"
	# set operating system id
	SPCD_OS_ID="$(spcd_grep_os ID)"
	case "${SPCD_OS_ID}" in
	"almalinux") SPCD_OS_ID="${SPCD_OS_ALMA}" ;;
	"alpine") SPCD_OS_ID="${SPCD_OS_ALPINE}" ;;
	"arch") SPCD_OS_ID="${SPCD_OS_ARCH}" ;;
	"debian") SPCD_OS_ID="${SPCD_OS_DEBIAN}" ;;
	"fedora") SPCD_OS_ID="${SPCD_OS_FEDORA}" ;;
	"rocky") SPCD_OS_ID="${SPCD_OS_ROCKY}" ;;
	"ubuntu") SPCD_OS_ID="${SPCD_OS_UBUNTU}" ;;
	*) spcd_error_os "SPCD_OS_ID" ;;
	esac
	# set operating system version
	case "${SPCD_OS_ID}" in
	"${SPCD_OS_ALMA}" | "${SPCD_OS_FEDORA}" | "${SPCD_OS_ROCKY}" | \
		"${SPCD_OS_ARCH}")
		SPCD_OS_VERSION=$(spcd_grep_os VERSION_ID |
			sed "s|^\([0-9]\+\)\..*|\1|")
		;;
	"${SPCD_OS_ALPINE}")
		SPCD_OS_VERSION=$(spcd_grep_os VERSION_ID |
			sed "s|^\([0-9]\+\.[0-9]\+\)\..*|\1|")
		;;
	"${SPCD_OS_DEBIAN}" | "${SPCD_OS_UBUNTU}")
		SPCD_OS_VERSION="$(spcd_grep_os VERSION_CODENAME)"
		;;
	*) ;;
	esac
	# check operating system version
	case "${SPCD_OS_ID}" in
	"${SPCD_OS_ALMA}" | "${SPCD_OS_ROCKY}")
		case "${SPCD_OS_VERSION}" in
		"8" | "9") ;;
		*) spcd_error_os "SPCD_OS_VERSION" ;;
		esac
		;;
	"${SPCD_OS_ALPINE}")
		case "${SPCD_OS_VERSION}" in
		"3.18" | "3.19") ;;
		*) spcd_error_os "SPCD_OS_VERSION" ;;
		esac
		;;
	"${SPCD_OS_ARCH}")
		case "${SPCD_OS_VERSION}" in
		"20231112" | "20240101") ;;
		*) spcd_error_os "SPCD_OS_VERSION" ;;
		esac
		;;
	"${SPCD_OS_DEBIAN}")
		case "${SPCD_OS_VERSION}" in
		"bookworm" | "bullseye") ;;
		*) spcd_error_os "SPCD_OS_VERSION" ;;
		esac
		;;
	"${SPCD_OS_FEDORA}")
		case "${SPCD_OS_VERSION}" in
		"39" | "40") ;;
		*) spcd_error_os "SPCD_OS_VERSION" ;;
		esac
		;;
	"${SPCD_OS_UBUNTU}")
		case "${SPCD_OS_VERSION}" in
		"jammy" | "noble") ;;
		*) spcd_error_os "SPCD_OS_VERSION" ;;
		esac
		;;
	*) ;;
	esac
	spcd_split
	spcd_echo "SPCD_OS_ID" "SPCD_OS_VERSION"
	# universal
	SPCD_DNS_FILE="/etc/resolv.conf"
	SPCD_PKG_CA="ca-certificates"
	SPCD_PKG_GIT="git"
	# TODO move to Python
	SPCD_PKG_RSYNC="rsync"
	SPCD_PYTHON_ALIAS="python3"
	spcd_split
	spcd_echo "SPCD_DNS_FILE" "SPCD_PKG_CA" "SPCD_PKG_GIT" "SPCD_PYTHON_ALIAS"
	# set ca command & root
	case "${SPCD_OS_ID}" in
	"${SPCD_OS_ALMA}" | "${SPCD_OS_FEDORA}" | "${SPCD_OS_ROCKY}")
		SPCD_CA_ROOT="/etc/pki/ca-trust/source/anchors"
		SPCD_CMD_CA="update-ca-trust"
		;;
	"${SPCD_OS_ALPINE}")
		SPCD_CA_ROOT="/usr/local/share/ca-certificates"
		SPCD_CMD_CA="update-ca-certificates"
		;;
	"${SPCD_OS_ARCH}")
		SPCD_CA_ROOT="/etc/ca-certificates/trust-source/anchors"
		SPCD_CMD_CA="update-ca-trust"
		;;
	"${SPCD_OS_DEBIAN}" | "${SPCD_OS_UBUNTU}")
		SPCD_CA_ROOT="/usr/local/share/ca-certificates"
		SPCD_CMD_CA="update-ca-certificates"
		;;
	*) ;;
	esac
	spcd_split
	spcd_echo "SPCD_CA_ROOT" "SPCD_CMD_CA"
	# set package manager
	case "${SPCD_OS_ID}" in
	"${SPCD_OS_ALPINE}")
		SPCD_PM="${SPCD_PM_APK}"
		;;
	"${SPCD_OS_DEBIAN}" | "${SPCD_OS_UBUNTU}")
		SPCD_PM="${SPCD_PM_APT}"
		;;
	"${SPCD_OS_ALMA}" | "${SPCD_OS_FEDORA}" | "${SPCD_OS_ROCKY}")
		SPCD_PM="${SPCD_PM_DNF}"
		;;
	"${SPCD_OS_ARCH}")
		SPCD_PM="${SPCD_PM_PACMAN}"
		;;
	*) ;;
	esac
	spcd_split
	spcd_echo "SPCD_PM"
	case "${SPCD_PM}" in
	"${SPCD_PM_DNF}")
		SPCD_PM_CLEAN="dnf clean all"
		SPCD_PM_INSTALL="dnf install --assumeyes"
		SPCD_PM_QUERY="rpm --query"
		SPCD_PM_UPDATE="dnf makecache"
		SPCD_PM_UPGRADE="dnf upgrade --assumeyes"
		SPCD_PKG_PKG=""
		SPCD_PM_CONF_PATH="/etc/dnf/dnf.conf"
		SPCD_PM_CONF_TEXT="\
[main]
best=True
clean_requirements_on_remove=True
gpgcheck=1
installonly_limit=3
skip_if_unavailable=False
"
		SPCD_PM_HTTPS_PATH="/etc/dnf/dnf.conf.d/https.conf"
		SPCD_PM_HTTPS_TEXT="\
sslverify=False
"
		;;
	"${SPCD_PM_APK}")
		SPCD_PM_CLEAN="apk cache purge"
		SPCD_PM_INSTALL="apk add"
		SPCD_PM_QUERY="apk info"
		SPCD_PM_UPDATE="apk update"
		SPCD_PM_UPGRADE="apk upgrade"
		SPCD_PKG_PKG=""
		SPCD_PM_CONF_PATH=""
		SPCD_PM_CONF_TEXT=""
		SPCD_PM_HTTPS_PATH="/etc/apk/repositories.d/https"
		SPCD_PM_HTTPS_TEXT="\
--no-verify
"
		;;
	"${SPCD_PM_PACMAN}")
		SPCD_PM_CLEAN="pacman --sync --clean --noconfirm"
		SPCD_PM_INSTALL="pacman --sync --noconfirm"
		SPCD_PM_QUERY="pacman --query"
		SPCD_PM_UPDATE="pacman --sync --refresh"
		SPCD_PM_UPGRADE="pacman --sync --sysupgrade --noconfirm"
		SPCD_PKG_PKG=""
		SPCD_PM_CONF_PATH=""
		SPCD_PM_CONF_TEXT=""
		SPCD_PM_HTTPS_PATH="/etc/pacman.d/https.conf"
		SPCD_PM_HTTPS_TEXT="\
SSLVerify = No
"
		;;
	"${SPCD_PM_APT}")
		SPCD_PM_CLEAN="apt-get clean"
		SPCD_PM_INSTALL="apt-get install --assume-yes"
		SPCD_PM_QUERY="dpkg-query --show"
		SPCD_PM_UPDATE="apt-get update"
		SPCD_PM_UPGRADE="apt-get upgrade --assume-yes"
		SPCD_PKG_PKG="apt-utils"
		SPCD_PM_CONF_PATH="/etc/apt/apt.conf.d/apt.conf"
		SPCD_PM_CONF_TEXT="\
Acquire::Check-Valid-Until True;
APT::Get::Show-Versions True;
APT::Install-Recommends False;
APT::Install-Suggests False;
Dir::Etc::SourceParts \"\";
"
		SPCD_PM_HTTPS_PATH="/etc/apt/apt.conf.d/https"
		SPCD_PM_HTTPS_TEXT="\
Acquire::https::Verify-Peer False;
"
		;;
	*) ;;
	esac
	spcd_split
	spcd_echo "SPCD_PM_CLEAN" \
		"SPCD_PM_INSTALL" "SPCD_PM_QUERY" "SPCD_PM_UPDATE" "SPCD_PM_UPGRADE"
	spcd_split
	spcd_echo "SPCD_PKG_PKG" "SPCD_PM_CONF_PATH" "SPCD_PM_HTTPS_PATH"
	# specific
	case "${SPCD_OS_ID}" in
	"${SPCD_OS_ALMA}")
		SPCD_URL_DEFAULT="https://repo.almalinux.org/almalinux"
		;;
	"${SPCD_OS_ALPINE}")
		SPCD_URL_DEFAULT="https://dl-cdn.alpinelinux.org/alpine"
		;;
	"${SPCD_OS_ARCH}")
		SPCD_URL_DEFAULT="https://geo.mirror.pkgbuild.com"
		;;
	"${SPCD_OS_DEBIAN}")
		SPCD_URL_DEFAULT="http://deb.debian.org/debian"
		;;
	"${SPCD_OS_FEDORA}")
		SPCD_URL_DEFAULT="http://download.example/pub/fedora/linux/releases"
		;;
	"${SPCD_OS_ROCKY}")
		SPCD_URL_DEFAULT="http://dl.rockylinux.org/\$contentdir"
		;;
	"${SPCD_OS_UBUNTU}")
		SPCD_URL_DEFAULT="http://archive.ubuntu.com/ubuntu"
		;;
	*) ;;
	esac
	SPCD_URL_CHOSEN="${SPCD_URL_DEFAULT}"
	case "${SPCD_OS_ID}" in
	"${SPCD_OS_ALMA}")
		[ -n "${SPCD_URL_ALMA}" ] && SPCD_URL_CHOSEN="${SPCD_URL_ALMA}"
		;;
	"${SPCD_OS_ALPINE}")
		[ -n "${SPCD_URL_ALPINE}" ] && SPCD_URL_CHOSEN="${SPCD_URL_ALPINE}"
		;;
	"${SPCD_OS_ARCH}")
		[ -n "${SPCD_URL_ARCH}" ] && SPCD_URL_CHOSEN="${SPCD_URL_ARCH}"
		;;
	"${SPCD_OS_DEBIAN}")
		[ -n "${SPCD_URL_DEBIAN}" ] && SPCD_URL_CHOSEN="${SPCD_URL_DEBIAN}" ||
			SPCD_URL_CHOSEN="https://deb.debian.org/debian"
		;;
	"${SPCD_OS_FEDORA}")
		[ -n "${SPCD_URL_FEDORA}" ] && SPCD_URL_CHOSEN="${SPCD_URL_FEDORA}" ||
			SPCD_URL_CHOSEN="https://rpmfind.net/linux/fedora/linux/releases"
		;;
	"${SPCD_OS_ROCKY}")
		[ -n "${SPCD_URL_ROCKY}" ] && SPCD_URL_CHOSEN="${SPCD_URL_ROCKY}" ||
			SPCD_URL_CHOSEN="https://dl.rockylinux.org/\$contentdir"
		;;
	"${SPCD_OS_UBUNTU}")
		[ -n "${SPCD_URL_UBUNTU}" ] && SPCD_URL_CHOSEN="${SPCD_URL_UBUNTU}" ||
			SPCD_URL_CHOSEN="https://ubuntu.mirrors.ovh.net/ubuntu"
		;;
	*) ;;
	esac
	spcd_split
	spcd_echo "SPCD_URL_DEFAULT" "SPCD_URL_CHOSEN"
	# set python command & package
	case "${SPCD_OS_ID}" in
	"${SPCD_OS_ALMA}" | "${SPCD_OS_ROCKY}")
		SPCD_PYTHON_COMMAND="python3.11"
		SPCD_PYTHON_PACKAGE="python3.11"
		;;
	"${SPCD_OS_ALPINE}")
		SPCD_PYTHON_COMMAND="python3.11"
		SPCD_PYTHON_PACKAGE="python3"
		;;
	"${SPCD_OS_ARCH}")
		SPCD_PYTHON_COMMAND="python3.12"
		SPCD_PYTHON_PACKAGE="python"
		;;
	"${SPCD_OS_DEBIAN}")
		case "${SPCD_OS_VERSION}" in
		"bookworm") SPCD_PYTHON_COMMAND="python3.11" ;;
		"bullseye") SPCD_PYTHON_COMMAND="python3.9" ;;
		*) ;;
		esac
		SPCD_PYTHON_PACKAGE="python3"
		;;
	"${SPCD_OS_FEDORA}")
		SPCD_PYTHON_COMMAND="python3.12"
		SPCD_PYTHON_PACKAGE="python3"
		;;
	"${SPCD_OS_UBUNTU}")
		case "${SPCD_OS_VERSION}" in
		"noble") SPCD_PYTHON_COMMAND="python3.12" ;;
		"jammy") SPCD_PYTHON_COMMAND="python3.10" ;;
		*) ;;
		esac
		SPCD_PYTHON_PACKAGE="python3"
		;;
	*) ;;
	esac
	# set python packages
	case "${SPCD_OS_ID}" in
	"${SPCD_OS_ALMA}" | "${SPCD_OS_FEDORA}" | "${SPCD_OS_ROCKY}")
		SPCD_PYTHON_PACKAGES="/usr/lib64/${SPCD_PYTHON_COMMAND}/site-packages"
		;;
	"${SPCD_OS_ALPINE}" | "${SPCD_OS_ARCH}")
		SPCD_PYTHON_PACKAGES="/usr/lib/${SPCD_PYTHON_COMMAND}/site-packages"
		;;
	"${SPCD_OS_DEBIAN}" | "${SPCD_OS_UBUNTU}")
		SPCD_PYTHON_PACKAGES="/usr/lib/${SPCD_PYTHON_ALIAS}/dist-packages"
		;;
	*) ;;
	esac
	spcd_split
	spcd_echo "SPCD_PYTHON_COMMAND" "SPCD_PYTHON_PACKAGE" "SPCD_PYTHON_PACKAGES"
	# variables
	[ -n "${SPCD_CA_1}" ] && SPCD_CA=true
	# continuous integration platform
	if [ -n "${GITHUB_ACTIONS}" ]; then
		# github → gitea → forgejo
		if [ -n "${GITHUB_SERVER_URL}" ]; then
			SPCD_PROJECT_ROOT="$(dirname "${GITHUB_SERVER_URL}")//"
			[ -n "${GITHUB_TOKEN}" ] &&
				SPCD_PROJECT_ROOT="${SPCD_PROJECT_ROOT}${GITHUB_TOKEN}@"
			SPCD_PROJECT_ROOT="${SPCD_PROJECT_ROOT}$(basename "${GITHUB_SERVER_URL}")"
		else
			spcd_error_ci "GITHUB_SERVER_URL"
		fi
		if [ -n "${GITHUB_REPOSITORY}" ]; then
			SPCD_PROJECT_PATH="$(dirname "${GITHUB_REPOSITORY}")"
			SPCD_PROJECT_NAME="$(basename "${GITHUB_REPOSITORY}")"
		else
			spcd_error_ci "GITHUB_REPOSITORY"
		fi
		if [ -n "${GITHUB_REF_NAME}" ]; then
			SPCD_PROJECT_BRANCH="${GITHUB_REF_NAME}"
		else
			spcd_error_ci "GITHUB_REF_NAME"
		fi
	elif [ -n "${GITLAB_CI}" ]; then
		# gitlab
		if [ -n "${CI_SERVER_PROTOCOL}" ]; then
			if [ -n "${CI_REGISTRY_USER}" ]; then
				if [ -n "${CI_REGISTRY_PASSWORD}" ]; then
					if [ -n "${CI_SERVER_FQDN}" ]; then
						SPCD_PROJECT_ROOT="${CI_SERVER_PROTOCOL}\
://${CI_REGISTRY_USER}:${CI_REGISTRY_PASSWORD}@${CI_SERVER_FQDN}"
						if [ -n "${CI_PROJECT_NAMESPACE}" ]; then
							SPCD_PROJECT_PATH="${CI_PROJECT_NAMESPACE}"
							if [ -n "${CI_PROJECT_NAME}" ]; then
								SPCD_PROJECT_NAME="${CI_PROJECT_NAME}"
							else
								spcd_error_ci "CI_PROJECT_NAME"
							fi
						else
							spcd_error_ci "CI_PROJECT_NAMESPACE"
						fi
					else
						spcd_error_ci "CI_SERVER_FQDN"
					fi
				else
					spcd_error_ci "CI_REGISTRY_PASSWORD"
				fi
			else
				spcd_error_ci "CI_REGISTRY_USER"
			fi
		else
			spcd_error_ci "CI_SERVER_PROTOCOL"
		fi
		if [ -n "${CI_COMMIT_BRANCH}" ]; then
			SPCD_PROJECT_BRANCH="${CI_COMMIT_BRANCH}"
		else
			spcd_error_ci "CI_COMMIT_BRANCH"
		fi
	else
		# unsupported
		spcd_error_ci "ø"
	fi
	[ -n "${SPCD_PROJECT_ROOT}" ] || spcd_error_ci "SPCD_PROJECT_ROOT"
	[ -n "${SPCD_PROJECT_PATH}" ] || spcd_error_ci "SPCD_PROJECT_PATH"
	[ -n "${SPCD_PROJECT_NAME}" ] || spcd_error_ci "SPCD_PROJECT_NAME"
	[ -n "${SPCD_PROJECT_BRANCH}" ] || spcd_error_ci "SPCD_PROJECT_BRANCH"
	#
	spcd_split
	spcd_echo "SPCD_CA"
	spcd_split
	spcd_echo "SPCD_PROJECT_ROOT" \
		"SPCD_PROJECT_PATH" "SPCD_PROJECT_NAME" "SPCD_PROJECT_BRANCH"
	# TODO move to Python
	case "${SPCD_PM}" in
	"${SPCD_PM_APK}" | "${SPCD_PM_APT}") SPCD_PKG_SSH="openssh-client" ;;
	"${SPCD_PM_DNF}") SPCD_PKG_SSH="openssh-clients" ;;
	"${SPCD_PM_PACMAN}") SPCD_PKG_SSH="openssh" ;;
	*) ;;
	esac
}

spcd_set_packages_repositories() {
	spcd_step "Set packages repositories"
	case "${SPCD_OS_ID}" in
	"${SPCD_OS_ALMA}")
		case "${SPCD_OS_VERSION}" in
		"8") spcd_spr__file="/etc/yum.repos.d/almalinux.repo" ;;
		"9") spcd_spr__file="/etc/yum.repos.d/almalinux-baseos.repo" ;;
		*) ;;
		esac
		spcd_sed "${spcd_spr__file}" \
			"|^mirrorlist|# mirrorlist|" \
			"|${SPCD_URL_DEFAULT}|${SPCD_URL_CHOSEN}|" \
			"|^# baseurl|baseurl|"
		;;
	"${SPCD_OS_ALPINE}")
		spcd_spr__file="/etc/apk/repositories"
		spcd_write "${spcd_spr__file}" "\
${SPCD_URL_CHOSEN}/v${SPCD_OS_VERSION}/main
${SPCD_URL_CHOSEN}/v${SPCD_OS_VERSION}/community
"
		;;
	"${SPCD_OS_DEBIAN}")
		spcd_spr__file="/etc/apt/sources.list"
		spcd_write "${spcd_spr__file}" "\
deb ${SPCD_URL_CHOSEN} ${SPCD_OS_VERSION} main
deb ${SPCD_URL_CHOSEN} ${SPCD_OS_VERSION}-backports main
deb ${SPCD_URL_CHOSEN} ${SPCD_OS_VERSION}-updates main
deb ${SPCD_URL_CHOSEN}-security ${SPCD_OS_VERSION}-security main
"
		;;
	"${SPCD_OS_ROCKY}")
		case "${SPCD_OS_VERSION}" in
		"8") spcd_spr__file="/etc/yum.repos.d/Rocky-BaseOS.repo" ;;
		"9") spcd_spr__file="/etc/yum.repos.d/rocky.repo" ;;
		*) ;;
		esac
		spcd_sed "${spcd_spr__file}" \
			"|^mirrorlist|# mirrorlist|" \
			"|${SPCD_URL_DEFAULT}|${SPCD_URL_CHOSEN}|" \
			"|^#baseurl|baseurl|"
		;;
	"${SPCD_OS_UBUNTU}")
		spcd_spr__file="/etc/apt/sources.list"
		spcd_write "${spcd_spr__file}" "\
deb ${SPCD_URL_CHOSEN} ${SPCD_OS_VERSION} main
deb ${SPCD_URL_CHOSEN} ${SPCD_OS_VERSION}-backports main
deb ${SPCD_URL_CHOSEN} ${SPCD_OS_VERSION}-updates main
deb ${SPCD_URL_CHOSEN} ${SPCD_OS_VERSION}-security main
"
		;;
	*) ;;
	esac
}

spcd_set_packages_configuration() {
	spcd_step "Set packages configuration"
	spcd_write "${SPCD_PM_CONF_PATH}" "${SPCD_PM_CONF_TEXT}"
	case "${SPCD_OS_ID}" in
	"${SPCD_OS_DEBIAN}" | "${SPCD_OS_UBUNTU}")
		export DEBIAN_FRONTEND="noninteractive"
		;;
	*) ;;
	esac
}

# agnostic steps

spcd_set_https_verification_off() {
	if [ -n "${SPCD_CA}" ] || [ "${SPCD_PM}" = "${SPCD_PM_APT}" ]; then
		spcd_step "Set HTTPS verification off"
		spcd_mkdir "$(dirname "${SPCD_PM_HTTPS_PATH}")"
		spcd_write "${SPCD_PM_HTTPS_PATH}" "${SPCD_PM_HTTPS_TEXT}"
	fi
}

spcd_set_dns_resolving() {
	spcd_step "Set DNS resolving"
	for spcd_sdr__server in ${SPCD_DNS}; do
		spcd_sdr__text="${spcd_sdr__text}\
nameserver ${spcd_sdr__server}
"
	done
	spcd_write "${SPCD_DNS_FILE}" "${spcd_sdr__text}"
}

spcd_update_packages_catalog() {
	spcd_step "Update packages catalog"
	${SPCD_PM_UPDATE} || exit
}

spcd_install_packages_tools() {
	spcd_step "Install packages tools"
	spcd_install_package "${SPCD_PKG_PKG}"
}

spcd_install_ca_certificates() {
	spcd_step "Install CA"
	spcd_install_package "${SPCD_PKG_CA}"
}

spcd_write_ca_certificates() {
	spcd_step "Write CA certificates"
	spcd_mkdir "${SPCD_CA_ROOT}"
	spcd_wcc__index=1
	eval "spcd_wcc__text=\"\${SPCD_CA_${spcd_wcc__index}}\""
	while [ -n "${spcd_wcc__text}" ]; do
		spcd_wcc__path="${SPCD_CA_ROOT}/${spcd_wcc__index}.crt"
		spcd_split
		spcd_write "${spcd_wcc__path}" "${spcd_wcc__text}"
		spcd_openssl "${spcd_wcc__path}"
		spcd_wcc__index=$((spcd_wcc__index + 1))
		eval "spcd_wcc__text=\"\${SPCD_CA_${spcd_wcc__index}}\""
	done
}

spcd_update_ca_certificates() {
	spcd_step "Update CA certificates"
	${SPCD_CMD_CA} || exit
}

spcd_set_https_verification_on() {
	spcd_step "Set HTTPS verification on"
	spcd_rm "${SPCD_PM_HTTPS_PATH}"
}

spcd_upgrade_packages() {
	spcd_step "Upgrade packages"
	${SPCD_PM_UPGRADE} || exit
}

spcd_install_git() {
	spcd_step "Install Git"
	spcd_install_package "${SPCD_PKG_GIT}"
}

spcd_install_python() {
	spcd_step "Install Python"
	spcd_install_package "${SPCD_PYTHON_PACKAGE}"
	spcd_split
	spcd_ln_python "${SPCD_PYTHON_COMMAND}"
}

# TODO move to Python
spcd_install_rsync() {
	spcd_step "Install Rsync"
	spcd_install_package "${SPCD_PKG_RSYNC}"
}

# TODO move to Python
spcd_install_ssh() {
	spcd_step "Install SSH"
	spcd_install_package "${SPCD_PKG_SSH}"
}

spcd_clean_packages_cache() {
	spcd_step "Clean packages cache"
	${SPCD_PM_CLEAN} || exit
}

spcd_install_python_modules() {
	spcd_step "Install Python modules"
	spcd_ipm__root="$(mktemp --directory)" || exit
	echo "→ ${spcd_ipm__root}"
	for spcd_ipm__repository in "${SPCD_GIT_MAIN}" "${SPCD_GIT_ROOT}"; do
		case "${spcd_ipm__repository}" in
		http*) spcd_ipm__url="${spcd_ipm__repository}" ;;
		/*) spcd_ipm__url="${SPCD_PROJECT_ROOT}${spcd_ipm__repository}" ;;
		*) spcd_ipm__url="\
${SPCD_PROJECT_ROOT}/${SPCD_PROJECT_PATH}/${spcd_ipm__repository}" ;;
		esac
		spcd_ipm__name="$(basename "${spcd_ipm__url}")"
		spcd_split
		echo "\
${spcd_ipm__url}
↓"
		git clone \
			"${spcd_ipm__url}" \
			"${spcd_ipm__root}/${spcd_ipm__name}" ||
			exit
		spcd_ipm__path="${spcd_ipm__root}/${spcd_ipm__name}/${spcd_ipm__name}"
		echo "\
${spcd_ipm__path}
↓
${SPCD_PYTHON_PACKAGES}"
		cp --recursive "${spcd_ipm__path}" "${SPCD_PYTHON_PACKAGES}" ||
			exit
	done
	spcd_split
	spcd_ls "${SPCD_PYTHON_PACKAGES}"
	spcd_split
	spcd_rm "${spcd_ipm__root}"
}

spcd_write_python_module() {
	spcd_step "Write Python module"
	for spcd_wpm__variable in \
		OS_ID OS_VERSION \
		PROJECT_ROOT PROJECT_PATH PROJECT_NAME \
		OPEN DOWN VERT SPLT __UP SHUT; do
		spcd_wpm__value="$(spcd_echo "SPCD_${spcd_wpm__variable}")"
		spcd_wpm__text="${spcd_wpm__text}${spcd_wpm__value}
"
	done
	spcd_write "${SPCD_PYTHON_PACKAGES}/env.py" "${spcd_wpm__text}
SPCD_STEP = $((SPCD_STEP + 1))
"
}

spcd_switch_to_python() {
	spcd_step "Switch to Python"
	spcd_stp__name="$(basename "${SPCD_GIT_MAIN}")"
	echo "\
${SPCD_PATH}
↓
${SPCD_PYTHON_PACKAGES}/${spcd_stp__name}"
	"${SPCD_PYTHON_ALIAS}" -m "${spcd_stp__name}" "${@}"
}

# functions

spcd_cat() {
	spcd_cat__file="${1}"
	if [ -n "${spcd_cat__file}" ]; then
		spcd_open "${spcd_cat__file}"
		cat "${spcd_cat__file}" || exit
		spcd_shut "${spcd_cat__file}"
	fi
}

spcd_echo() {
	if [ -n "${1}" ]; then
		for spcd_echo__name in "${@}"; do
			spcd_echo__text=""
			eval "spcd_echo__text=\"\${${spcd_echo__name}}\""
			echo "${spcd_echo__name} = \"${spcd_echo__text}\""
		done
	fi
}

spcd_error_ci() {
	echo "× CI: ${*}"
	exit "${SPCD_ERROR_CI}"
}

spcd_error_os() {
	spcd_error_os__variable="${1}"
	printf "× OS: "
	spcd_echo "${spcd_error_os__variable}"
	exit "${SPCD_ERROR_OS}"
}

spcd_grep_os() {
	spcd_grep_os__variable="${1}"
	[ -n "${spcd_grep_os__variable}" ] &&
		grep "^${spcd_grep_os__variable}=" "/etc/os-release" |
		sed "s|^${spcd_grep_os__variable}=||" |
			sed "s|^\"\(.*\)\"$|\1|"
}

spcd_install_package() {
	spcd_install_package__name="${1}"
	if [ -n "${spcd_install_package__name}" ]; then
		${SPCD_PM_INSTALL} "${spcd_install_package__name}" || exit
	fi
}

spcd_ln_python() {
	spcd_ln_python__command="${1}"
	if [ -n "${spcd_ln_python__command}" ]; then
		echo "→ ${SPCD_PYTHON_ALIAS} → ${spcd_ln_python__command}"
		ln -f -s "${spcd_ln_python__command}" \
			"/usr/bin/${SPCD_PYTHON_ALIAS}" || exit
	fi
}

spcd_ls() {
	spcd_ls__path="${1}"
	if [ -n "${spcd_ls__path}" ]; then
		spcd_open "${spcd_ls__path}"
		ls -a -l "${spcd_ls__path}" || exit
		spcd_shut "${spcd_ls__path}"
	fi
}

spcd_mkdir() {
	spcd_mkdir__path="${1}"
	if [ -n "${spcd_mkdir__path}" ]; then
		echo "→ ${spcd_mkdir__path}"
		mkdir --parents "${spcd_mkdir__path}" || exit
	fi
}

spcd_open() {
	echo "${SPCD_OPEN}${*}"
}

spcd_openssl() {
	spcd_openssl__file="${1}"
	if [ -f "${spcd_openssl__file}" ]; then
		openssl x509 \
			-in "${spcd_openssl__file}" \
			-noout -text ||
			exit
	fi
}

spcd_rm() {
	spcd_rm__path="${1}"
	if [ -e "${spcd_rm__path}" ]; then
		echo "← ${spcd_rm__path}"
		rm -r "${spcd_rm__path}" || exit
	fi
}

spcd_sed() {
	spcd_sed__file="${1}"
	shift
	if [ -f "${spcd_sed__file}" ]; then
		spcd_cat "${spcd_sed__file}"
		for spcd_sed__regex in "${@}"; do
			sed --in-place "s${spcd_sed__regex}g" "${spcd_sed__file}" &&
				spcd_cat "${spcd_sed__file}" || exit
		done
	fi
}

spcd_shut() {
	echo "${SPCD_SHUT}${*}"
}

spcd_split() {
	echo "${SPCD_SPLT}"
}

spcd_step() {
	SPCD_STEP=$((SPCD_STEP + 1))
	echo "\
${SPCD_DOWN}
${SPCD_VERT} ${SPCD_STEP} ${*}
${SPCD___UP}"
}

spcd_write() {
	spcd_write__file="${1}"
	spcd_write__text="${2}"
	if [ -n "${spcd_write__file}" ]; then
		[ -f "${spcd_write__file}" ] && spcd_cat "${spcd_write__file}"
		echo "→ ${spcd_write__file}"
		printf "%s" "${spcd_write__text}" >"${spcd_write__file}" || exit
		spcd_cat "${spcd_write__file}"
	fi
}

# constants

SPCD_BOX_DOWN="╭"
SPCD_BOX_LEFT="╴"
SPCD_BOX_RIGHT="╶"
SPCD_BOX_UP="╰"
SPCD_BOX_VERTICAL="│"

SPCD_ERROR_CI=2
SPCD_ERROR_OS=1

SPCD_OS_ALMA="alma"
SPCD_OS_ALPINE="alpine"
SPCD_OS_ARCH="arch"
SPCD_OS_DEBIAN="debian"
SPCD_OS_FEDORA="fedora"
SPCD_OS_ROCKY="rocky"
SPCD_OS_UBUNTU="ubuntu"

SPCD_PM_APK="apk"
SPCD_PM_APT="apt"
SPCD_PM_DNF="dnf"
SPCD_PM_PACMAN="pacman"

SPCD_HORIZONTAL="────╌╌╌╌┄┄┄┄┈┈┈┈"

SPCD_OPEN="${SPCD_BOX_DOWN}${SPCD_BOX_LEFT}"
SPCD_DOWN="${SPCD_BOX_DOWN}${SPCD_HORIZONTAL}"
SPCD_VERT="${SPCD_BOX_VERTICAL}"
SPCD_SPLT="${SPCD_BOX_RIGHT}${SPCD_HORIZONTAL}"
SPCD___UP="${SPCD_BOX_UP}${SPCD_HORIZONTAL}"
SPCD_SHUT="${SPCD_BOX_UP}${SPCD_BOX_LEFT}"

# run
spcd_main "${@}"
