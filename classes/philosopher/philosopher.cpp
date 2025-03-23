#include "philosopher.h"

std::mutex coutMutex;

Philosopher::Philosopher(const int id, std::vector<std::unique_ptr<std::counting_semaphore<1>>>& forks)
    : id(id), forks(forks) {}

[[noreturn]] void Philosopher::operator()() const {
    while (true) {
        thinking();
        pickUp();
        eating();
        putDown();
    }
}

void Philosopher::thinking() const {
    std::ostringstream log;
    log << "Philosopher " << id << " is thinking" << std::endl;
    {
        std::lock_guard<std::mutex> lock(coutMutex);
        std::cout << log.str();
    }
    std::this_thread::sleep_for(std::chrono::seconds(static_cast<long>(1)));
}

void Philosopher::eating() const {
    std::ostringstream log;
    log << "Philosopher " << id << " is eating" << std::endl;

    {
        std::this_thread::sleep_for(std::chrono::milliseconds(static_cast<long>(10)));
        std::lock_guard<std::mutex> lock(coutMutex);
        std::cout << log.str();
    }
    std::this_thread::sleep_for(std::chrono::seconds(static_cast<long>(5)));
}

void Philosopher::pickUp() const {
    forks[id]->acquire();
    forks[(id + 1) % forks.size()]->acquire();
}

void Philosopher::putDown() const {
    forks[id]->release();
    forks[(id + 1) % forks.size()]->release();
}
