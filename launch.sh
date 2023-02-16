if [ -z "${MXRP_ENTRYPOINT}" ]; then
    echo "Running $MXRP_ENTRYPOINT"
    eval "${MXRP_ENTRYPOINT}"
fi