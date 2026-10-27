#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <unistd.h>

/* Chapter 19: touch one int per page and time it. */
int main(int argc, char *argv[])
{
    int i, t;
    int npages, ntrials;
    int jump;
    int *a;
    long pagesize;
    struct timeval start, end;
    double seconds, ns;

    if (argc != 3) {
        printf("usage: %s npages ntrials\n", argv[0]);
        return 1;
    }

    npages = atoi(argv[1]);
    ntrials = atoi(argv[2]);
    pagesize = sysconf(_SC_PAGESIZE);
    jump = pagesize / sizeof(int);

    a = (int *) malloc(npages * jump * sizeof(int));
    if (a == NULL) {
        printf("malloc failed\n");
        return 1;
    }

    /* fill the pages first so the timer does not include page faults */
    for (i = 0; i < npages * jump; i += jump) {
        a[i] = 0;
    }

    gettimeofday(&start, NULL);
    for (t = 0; t < ntrials; t++) {
        for (i = 0; i < npages * jump; i += jump) {
            a[i] += 1;
        }
    }
    gettimeofday(&end, NULL);

    seconds = (end.tv_sec - start.tv_sec)
            + (end.tv_usec - start.tv_usec) / 1000000.0;
    ns = (seconds / ((double) ntrials * (double) npages)) * 1000000000.0;

    /* print a[0] so the compiler keeps the loop */
    printf("pages=%d trials=%d pagesize=%ld ns_per_access=%.3f last=%d\n",
           npages, ntrials, pagesize, ns, a[0]);

    free(a);
    return 0;
}
