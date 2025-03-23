#ifndef PHILOSOPHER_H
#define PHILOSOPHER_H

#include <vector>
#include <semaphore>
#include <thread>
#include <chrono>
#include <iostream>
#include <mutex>

class Philosopher {
public:
    Philosopher(int id, std::vector<std::unique_ptr<std::counting_semaphore<1>>>& forks);
    [[noreturn]] void operator()() const;

private:
    void thinking() const;
    void eating() const;
    void pickUp() const;
    void putDown() const;

    int id;
    std::vector<std::unique_ptr<std::counting_semaphore<1>>>& forks;
};

#endif // PHILOSOPHER_H