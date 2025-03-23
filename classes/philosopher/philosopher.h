#pragma once

#include <vector>
#include <semaphore>
#include <chrono>

/// Class to represent philosopher for dinning philosopher problem.
/// Each philosopher on start have infinite loop to represent work.
class Philosopher {
public:
    /// Constructor to initialize the philosopher with an ID and a reference to the forks
    Philosopher(int id, std::vector<std::unique_ptr<std::counting_semaphore<1>>>& forks);

    /// Overloaded function call operator to start the philosopher's actions
    [[noreturn]] void operator()() const;

private:
    /// This function simulates the philosopher thinking. Thinking takes 1 second.
    void thinking() const;

    /// This function simulates the philosopher eating. Eating takes 5 seconds.
    void eating() const;

    /// This function simulates the philosopher picking up forks.
    void pickUp() const;

    /// This function simulates the philosopher putting forks down.
    void putDown() const;

    int id;
    std::vector<std::unique_ptr<std::counting_semaphore<1>>>& forks;
};