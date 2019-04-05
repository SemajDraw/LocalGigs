import { Component } from '@angular/core';
import { NavController} from 'ionic-angular';
import { LoginPage } from "../login/login";
import { App } from "ionic-angular";
import { RestProvider} from "../../providers/rest/rest";

@Component({
  selector: 'page-profile',
  templateUrl: 'profile.html'
})
export class ProfilePage {

  userDetails: any;
  gigList: any;
  user = {
    "first_name": "",
    "last_name": ""
  };

  constructor(public navCtrl: NavController, private app: App, public restProvider: RestProvider) {
    // Get the users details from localstorage and store them in the user object
    const storedUser = JSON.parse(localStorage.getItem('user'));
    this.userDetails = storedUser;

    this.user.first_name = this.userDetails.first_name;
    this.user.last_name = this.userDetails.last_name;
  }

  ionViewDidLoad() {
    this.getSavedEvents();
  }

  getSavedEvents() {
    // Try and search for gigs through the django api
    // If successful populate list in template
    try {
      this.restProvider.getSavedEvents()
        .then(data => {
          this.gigList = data;
          console.log(this.gigList);
        });
    }
    catch (e) {
      console.log(e)
    }
  }

  // locateVenue(venueId){
  //   // Try and search for venue information
  //   // If successful create an event that publishes
  //   // The details of the venue so the map page can listen for it
  //   try {
  //     this.restProvider.venueInfo(venueId)
  //       .then(data => {
  //         this.events.publish('venue:locate', data);
  //         this.navCtrl.parent.select(3);
  //         console.log(data);
  //       });
  //   }
  //   catch (e) {
  //     console.log(e)
  //   }
  // }

  // Clear local storage, log user out and nav to login
  logOut() {
    this.purgeUser();
    this.app.getRootNav().setRoot(LoginPage);
    this.navCtrl.push(LoginPage);
  }

  purgeUser() {
    // Clear the local storage and navigate to the login page
    localStorage.removeItem('user');
    localStorage.clear();
  }


}
