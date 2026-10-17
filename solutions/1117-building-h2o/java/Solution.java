import java.util.concurrent.Semaphore;

class H2O {
    private Semaphore semH;
    private Semaphore semO;
    private int hCount;
    private final Object lock = new Object();

    public H2O() {
        semH = new Semaphore(2);
        semO = new Semaphore(0);
        hCount = 0;
    }

    public void hydrogen(Runnable releaseHydrogen) throws InterruptedException {
        semH.acquire();
        releaseHydrogen.run();
        synchronized (lock) {
            hCount++;
            if (hCount == 2) {
                hCount = 0;
                semO.release();
            }
        }
    }

    public void oxygen(Runnable releaseOxygen) throws InterruptedException {
        semO.acquire();
        releaseOxygen.run();
        semH.release(2);
    }
}

class Solution extends H2O {
}
