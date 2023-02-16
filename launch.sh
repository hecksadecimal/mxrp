if [[ ! -n "${MXRP_ENTRYPOINT}" ]]; then
    echo "Running $MXRP_ENTRYPOINT"
    eval "${MXRP_ENTRYPOINT}"
else
    echo "MXRP_ENTRYPOINT undefined!"
fi 2>&1