import java.util.Objects;

/**
 * Single-file Java 17 reference for Codility-style POST /users validation.
 * <p>
 * Spec (from task): 400 if name or age missing, name &gt; 32 chars, or age &lt; 16;
 * otherwise call repository.save and respond with 201 and the saved UserDto body.
 * Wrong JSON types for age are handled by the framework (age ends up null → 400).
 */
public class UserApiSingleFile {

    /** Mirrors assessment DTO; framework sets fields from JSON. */
    public static class UserDto {
        private String name;
        private Integer age;

        public UserDto() {}

        public UserDto(String name, Integer age) {
            this.name = name;
            this.age = age;
        }

        public String getName() {
            return name;
        }

        public Integer getAge() {
            return age;
        }

        public void setName(String name) {
            this.name = name;
        }

        public void setAge(Integer age) {
            this.age = age;
        }
    }

    /** Assume save never throws; return value is the JSON body on success. */
    public interface UserRepository {
        UserDto save(UserDto user);
    }

    public static final class ValidationResult {
        private final int status;
        private final UserDto body;

        private ValidationResult(int status, UserDto body) {
            this.status = status;
            this.body = body;
        }

        public static ValidationResult badRequest() {
            return new ValidationResult(400, null);
        }

        public static ValidationResult created(UserDto saved) {
            return new ValidationResult(201, Objects.requireNonNull(saved));
        }

        public int status() {
            return status;
        }

        public UserDto body() {
            return body;
        }
    }

    /**
     * Core logic to drop into {@code UserRestController#create} (replace the 500 stub).
     * Map: 400 → ResponseEntity.badRequest().build(), 201 → ResponseEntity.status(CREATED).body(dto).
     */
    public static ValidationResult handleCreate(UserDto user, UserRepository repository) {
        if (user == null || user.getName() == null || user.getAge() == null) {
            return ValidationResult.badRequest();
        }
        if (user.getName().length() > 32) {
            return ValidationResult.badRequest();
        }
        if (user.getAge() < 16) {
            return ValidationResult.badRequest();
        }
        return ValidationResult.created(repository.save(user));
    }

    /** Runnable checks without Spring — compile: javac --release 17 UserApiSingleFile.java */
    public static void main(String[] args) {
        UserRepository repo = u -> {
            // stand-in persistence: return same object (or a copy if you prefer)
            return u;
        };

        UserDto ok = new UserDto("John Doe", 19);
        System.out.println(handleCreate(ok, repo).status()); // 201

        UserDto missingAge = new UserDto("John Doe", null);
        System.out.println(handleCreate(missingAge, repo).status()); // 400

        UserDto longName = new UserDto("a".repeat(33), 20);
        System.out.println(handleCreate(longName, repo).status()); // 400

        UserDto tooYoung = new UserDto("Jane", 13);
        System.out.println(handleCreate(tooYoung, repo).status()); // 400
    }
}

/*
 * --- Replace ONLY create() inside UserRestController (names/signatures fixed by template) ---

    @PostMapping
    public ResponseEntity<UserDto> create(@RequestBody UserDto user) {

        // Rule 1: missing fields
        if (user == null || user.getName() == null || user.getAge() == null) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }

        // Rule 2: name too long
        if (user.getName().length() > 32) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }

        // Rule 3: age < 16
        if (user.getAge() < 16) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST).build();
        }

        // Rule 4: valid → save and return 201 with body
        UserDto savedUser = repository.save(user);

        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(savedUser);
    }

 * ResponseEntity.badRequest().build() is equivalent to BAD_REQUEST above.
 * -----------------------------------------------------------------------------
 */
