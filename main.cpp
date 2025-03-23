#include <vector>
#include <semaphore>
#include <thread>
#include "../SO2/classes/philosopher/philosopher.h"

int main(int argc, char* argv[]) {
    const int numPhilosophers = std::stoi(argv[1]);
    std::vector<std::thread> philosophers;
    std::vector<std::unique_ptr<std::counting_semaphore<1>>> forks;

    for (int i = 0; i < numPhilosophers; ++i) {
        forks.emplace_back(std::make_unique<std::counting_semaphore<1>>(1));
    }

    for (int i = 0; i < numPhilosophers; ++i) {
        philosophers.emplace_back(Philosopher(i, forks));
    }

    for (auto& p : philosophers) {
        p.join();
    }

    return 0;
}