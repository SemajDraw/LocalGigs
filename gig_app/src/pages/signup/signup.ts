import {Component, ViewChild} from '@angular/core';
import { IonicPage, NavController, NavParams } from 'ionic-angular';
import { RestProvider } from "../../providers/rest/rest";
import {LoginPage} from "../login/login";

/**
 * Generated class for the SignupPage page.
 *
 * See https://ionicframework.com/docs/components/#navigation for more info on
 * Ionic pages and navigation.
 */

@IonicPage()
@Component({
  selector: 'page-signup',
  templateUrl: 'signup.html',
})
export class SignupPage {

  @ViewChild('username') username;
  @ViewChild('email') email;
  @ViewChild('firstName') firstName;
  @ViewChild('lastName') lastName;
  @ViewChild('password') password;
  @ViewChild('passwordCon') passwordCon;

  constructor(public navCtrl: NavController, public navParams: NavParams,
              public restProvider: RestProvider) {
  }

  signUp() {
    // Try and register the rest provider
    // If successful navigate to the login page
    try {
      this.restProvider.userSignUp(this.username.value, this.email.value, this.firstName.value,
                                  this.lastName.value, this.password.value, this.passwordCon.value)
        .then(data => { console.log(data); });

      this.navCtrl.push(LoginPage);
    }
    catch (e) {
      console.log(e)
    }
  }

}
