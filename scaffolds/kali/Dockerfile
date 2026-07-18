FROM kalilinux/kali-rolling

ARG KALI_PROFILE=web

RUN set -eux; \
    case "${KALI_PROFILE}" in \
      minimal) packages="ca-certificates curl iproute2 iputils-ping dnsutils netcat-traditional" ;; \
      web) packages="ca-certificates curl dirb dnsutils iproute2 iputils-ping netcat-traditional nikto nmap sqlmap wget whatweb" ;; \
      network) packages="ca-certificates curl dnsutils iproute2 iputils-ping netcat-traditional nmap tcpdump traceroute" ;; \
      *) echo "Perfil Kali desconhecido: ${KALI_PROFILE}" >&2; exit 1 ;; \
    esac; \
    export DEBIAN_FRONTEND=noninteractive; \
    apt-get update; \
    apt-get install --no-install-recommends -y ${packages}; \
    rm -rf /var/lib/apt/lists/*; \
    useradd --create-home --shell /bin/bash cyberlab

USER cyberlab
WORKDIR /home/cyberlab
