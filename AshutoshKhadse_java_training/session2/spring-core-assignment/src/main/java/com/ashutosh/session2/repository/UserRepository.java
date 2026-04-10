package com.ashutosh.session2.repository;

import com.ashutosh.session2.model.User;
import org.springframework.stereotype.Repository;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.concurrent.atomic.AtomicLong;

@Repository
public class UserRepository {

    private final List<User>     users   = new CopyOnWriteArrayList<>();
    private final AtomicLong     idSeq   = new AtomicLong(1);

    public List<User> findAll() {
        return new ArrayList<>(users);
    }

    public Optional<User> findById(Long id) {
        return users.stream()
                .filter(u -> u.getId().equals(id))
                .findFirst();
    }

    public User save(User user) {
        user.setId(idSeq.getAndIncrement());
        users.add(user);
        return user;
    }
}

