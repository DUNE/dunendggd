filename=$1
nevents=$2
outfilename="/exp/dune/data/users/${USER}/dunendggd/plot_true_particles/$(basename $filename).root"
make && nice -20 ./plot_true_particles $filename $nevents && python simply_draw_everything.py $outfilename
