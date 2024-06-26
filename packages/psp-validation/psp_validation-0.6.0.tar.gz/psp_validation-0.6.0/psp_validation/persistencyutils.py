"""Bundle of tools to help with persistifying data."""

import numpy as np


def dump_raw_traces_to_HDF5(h5file, data):  # noqa: N802 (function-lowercase)
    """Dump a set of simulated psp traces to an HDF5 file.

    Args:
    h5file: an h5py.File writable object
    data: array containing all the trace raw data

    The data format is:

    /traces/<pair>

    Each data corresponds to a synaptic pair and sample contains an array of \
    shape (nsim, 2, npoints) where nsim is the number of simulations run for \
    a given pair, 2 corresponds to arrays with voltage and time measurements, \
    and npoints is the length of those two arrays. Each pair group has \
    attributes 'gid_pre' and 'gid_post' with the GIDs of each cell in the pair.

    Access example:

    pair0_rep1 = hf['/traces/a42-a43'][1]
    pair_0_rep0_v = hf['/traces/a42-a43'][0][0]
    pair_0_rep0_t = hf['/traces/a42-a43'][0][1]
    pair_0_pre_gid = hf['/traces/a42-a43'].attrs['gid_pre']
    pair_0_post_gid = hf['/traces/a42-a43'].attrs['gid_post']

    """
    for pair in data:
        traces = [(t[0], t[1]) for t in pair]  # strip out gids
        pre_gid, post_gid = pair[0][2]
        group_name = f"/traces/a{pre_gid}-a{post_gid}"
        h5file[group_name] = np.array(traces)
        h5file[group_name].attrs["gid_pre"] = pre_gid
        h5file[group_name].attrs["gid_post"] = post_gid


def dump_pair_traces(h5file, traces, average, pre_gid, post_gid):
    """Dump a set of simulated psp traces to an HDF5 file.

    Args:
        h5file: writable h5py.File
        traces: N x 2 x T numpy array with trials voltage (or current) traces (V_k (or I_k), t_k)
        average: 2 x T numpy array with averaged / filtered trace (V_mean, t)
        pre_gid: presynaptic GID
        post_gid: postsynaptic GID
        data: array containing all the trace raw data

    The data format is:

    /traces
       /<pair-id>
           /trials   [N x 2 x T]
           /average  [2 x T]

    Each pair group has attributes 'pre_gid' and 'post_gid'.
    """
    group = h5file.create_group(
        f"/traces/{pre_gid.population}_{pre_gid.id}-{post_gid.population}_{post_gid.id}",
    )
    group.attrs["pre_id"] = pre_gid.id
    group.attrs["pre_population"] = pre_gid.population
    group.attrs["post_id"] = post_gid.id
    group.attrs["post_population"] = post_gid.population
    group["trials"] = traces
    if average is not None:
        group["average"] = average
