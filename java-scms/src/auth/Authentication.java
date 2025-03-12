package auth;

import org.mindrot.jbcrypt.BCrypt;

public class Authentication {
    public static String encryptPassword(String password) {
        return BCrypt.hashpw(password, BCrypt.gensalt());
    }

    public static boolean checkPassword(String password, Map<String, String> row) {
        return BCrypt.checkpw(password, row.get('password'));
    }
}
