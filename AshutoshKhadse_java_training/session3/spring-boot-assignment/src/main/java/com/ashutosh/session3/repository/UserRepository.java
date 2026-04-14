package com.ashutosh.session3.repository;

import com.ashutosh.session3.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicLong;
// Telling Spring this is our data access layer so it can manage it as a bean
@Repository
public class UserRepository {

    // Thread-safe list to handle concurrent API access
    private final List<User> users = new CopyOnWriteArrayList<>();

    // Starting our auto-increment counter at 16 since I'm hardcoding 15 users below.
    // Using AtomicLong to make sure ID generation is also thread-safe.
    private final AtomicLong idCounter = new AtomicLong(16);

    // I added this constructor to preload some dummy data when the app starts.
    // It makes testing our GET and filter APIs much easier without having to manually POST users every time.
    public UserRepository() {
        // Initialize with 15 dummy users
        users.add(new User(1L, "Priya", 30, "USER", "priya@example.com"));
        users.add(new User(2L, "Rahul", 25, "ADMIN", "rahul@example.com"));
        users.add(new User(3L, "priya", 22, "GUEST", "priya.guest@example.com")); // Testing case-insensitivity
        users.add(new User(4L, "Amit", 30, "USER", "amit@example.com"));
        users.add(new User(5L, "Sneha", 28, "MANAGER", "sneha@example.com"));
        users.add(new User(6L, "Karan", 35, "USER", "karan@example.com"));
        users.add(new User(7L, "Arjun", 40, "MANAGER", "arjun@example.com"));
        users.add(new User(8L, "Meera", 27, "USER", "meera@example.com"));
        users.add(new User(9L, "Vikram", 33, "ADMIN", "vikram@example.com"));
        users.add(new User(10L, "Divya", 29, "USER", "divya@example.com"));
        users.add(new User(11L, "Rohan", 24, "GUEST", "rohan@example.com"));
        users.add(new User(12L, "Anjali", 31, "USER", "anjali@example.com"));
        users.add(new User(13L, "Suresh", 45, "MANAGER", "suresh@example.com"));
        users.add(new User(14L, "Neha", 26, "ADMIN", "neha@example.com"));
        users.add(new User(15L, "Aditya", 28, "USER", "aditya@example.com"));
    }

    // I'm returning a brand-new list containing our users here.
    // I read that it's a good practice so other parts of the app can't accidentally modify our main database list so i implemented it
    public List<User> findAll() {
        return new ArrayList<>(users);
    }

    // Simple ID generation for our in-memory list.
    // If they are a brand-new user (no ID yet), we give them the next available number.
    public void save(User user) {
        if (user.getId() == null) {
            user.setId(idCounter.getAndIncrement());
        }
        users.add(user);
    }

    // Using Java Streams to quickly search for a matching ID.
    // Returning an Optional just in case the ID doesn't exist, which helps avoid those scary NullPointerExceptions later
    public Optional<User> findById(Long id) {
        return users.stream()
                .filter(user -> user.getId().equals(id))
                .findFirst();
    }

    // removeIf deletes the user if the ID matches and returns true if it actually deleted someone.
    // The service layer can use that boolean to know if the deletion was successful
    public boolean deleteById(Long id) {
        return users.removeIf(user -> user.getId().equals(id));
    }
}