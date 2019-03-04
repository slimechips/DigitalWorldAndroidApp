package sutd.digitalworld1d;

import java.util.HashMap;
import java.util.Map;

public class User {

    public String userName;
    public String email;
    public String userId;

    public User(String userName, String email, String userId) {
        this.userName = userName;
        this.email = email;
        this.userId = userId;
    }

    public Map<String, String> toMap () {
        HashMap result = new HashMap();
        result.put("user_name", this.userName);
        result.put("email", this.email);
        result.put("user_id", this.userId);
        return result;
    }
}
