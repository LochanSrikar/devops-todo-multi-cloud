package com.example.user;

import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataBootstrap implements CommandLineRunner {
    private final UserRepository repo;

    public DataBootstrap(UserRepository repo) {
        this.repo = repo;
    }

    @Override
    public void run(String... args) {
        if (repo.count() == 0) {  // Add data only if DB is empty
            User testUser = new User();
            testUser.setId(1L);
            testUser.setName("Test User");
            testUser.setToken("test");
            repo.save(testUser);
        }
    }
}