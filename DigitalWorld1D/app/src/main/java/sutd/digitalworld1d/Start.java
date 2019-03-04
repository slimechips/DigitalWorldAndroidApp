package sutd.digitalworld1d;

import android.content.Intent;
import android.os.Bundle;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;

import com.firebase.ui.auth.AuthUI;
import com.firebase.ui.auth.IdpResponse;
import com.google.firebase.FirebaseApp;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.auth.FirebaseUser;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;


import java.util.Arrays;
import java.util.List;

public class Start extends AppCompatActivity {

    public static List<AuthUI.IdpConfig> providers = Arrays.asList(
            new AuthUI.IdpConfig.EmailBuilder().build()
    );

    public static FirebaseUser user;
    public static final int RC_SIGN_IN = 123;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_start);
        Toolbar toolbar = findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);
        FirebaseApp.initializeApp(this);

    }

    public void SignIn(View view) {
        if (user == null) {
            startActivityForResult(
                    AuthUI.getInstance()
                            .createSignInIntentBuilder()
                            .setAvailableProviders(providers)
                            .build(),
                    RC_SIGN_IN);
        }
        else
        {
            startActivity(new Intent(Start.this, ChooseStallActivity.class));
            finish();
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (requestCode == RC_SIGN_IN) {
            IdpResponse response = IdpResponse.fromResultIntent(data);

            if (resultCode == RESULT_OK) {
                // Successfully signed in
                user = FirebaseAuth.getInstance().getCurrentUser();
                addNewUserToDatabase(user.getDisplayName(), user.getEmail(), user.getUid());
                startActivity(new Intent(Start.this, ChooseStallActivity.class));
                finish();
            } else {
                Toast.makeText(getApplicationContext(),
                        "Sign in failed", Toast.LENGTH_SHORT).show();
            }
        }
    }

    public static void addNewUserToDatabase(String _name, String _email, String _uid) {
        User _userToAdd = new User(_name, _email, _uid);
        FirebaseDatabase _database = FirebaseDatabase.getInstance();
        DatabaseReference _mDatabase = _database.getReference();
        _mDatabase.child("Users").child(_uid).setValue(_userToAdd.toMap());
    }

}
