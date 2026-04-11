package com.ashutosh.session2.repository;

import com.ashutosh.session2.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicLong;

// Telling Spring that this class is in charge of handling our data
@Repository
public class UserRepository {

    // Using a special thread-safe list so we don't get errors if multiple requests happen at the same time
    private final List<User>     users   = new CopyOnWriteArrayList<>();
    // This is  auto-increment counter for User IDs, also thread-safe
    private final AtomicLong     idSeq   = new AtomicLong(1);

    // To get all the users we have saved so far
    public List<User> findAll() {
        // Returning a new list so no one can accidentally mess up our main 'users' list
        return new ArrayList<>(users);
    }

    // to look up a user by their ID
    public Optional<User> findById(Long id) {
        return users.stream()
                .filter(u -> u.getId().equals(id))
                .findFirst();
    }

    // To save a new user into our temporary memory "database"
    public User save(User user) {
        // Give the user a new unique ID, then increase the counter up for the next person
        user.setId(idSeq.getAndIncrement());
        users.add(user);
        return user;
    }
}

