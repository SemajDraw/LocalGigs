import {Component, ViewChild} from '@angular/core';
import {IonicPage, NavController, NavParams} from 'ionic-angular';
import {SignupPage} from "../signup/signup";
import { RestProvider } from "../../providers/rest/rest";
import {TabsPage} from "../tabs/tabs";


@IonicPage()
@Component({
  selector: 'page-login',
  templateUrl: 'login.html',
})
export class LoginPage {

  userData: any;
  user = {
    "token": "",
    "first_name": "",
    "last_name": ""
  };
  @ViewChild('email') email;
  @ViewChild('password') password;

  constructor(public navCtrl: NavController, public navParams: NavParams,
              public restProvider: RestProvider) {

    try {
      const storedUser = JSON.parse(localStorage.getItem('user'));
      let userDetails = storedUser;

      if (userDetails.token != undefined){
        this.navCtrl.setRoot(TabsPage);
        this.navCtrl.push(TabsPage);
      }
    }
    catch (e) {
      console.log('no user signed in')
    }
  }

  logIn() {
    // Try and log user in through the rest provider
    // If successful store user and navigate to the profile page
    try {
      this.restProvider.userLogIn(this.email.value, this.password.value)
        .then(data => {
          this.userData = data;
          if(this.userData) {
            localStorage.setItem('user', JSON.stringify(data));
            this.navCtrl.setRoot(TabsPage);
            this.navCtrl.push(TabsPage);
          }
        });
    }
    catch (e) {
      console.log(e)
    }
  }

  // Navigate to the register page
  navRegisterPage() {
    this.navCtrl.push(SignupPage);
  }


}
