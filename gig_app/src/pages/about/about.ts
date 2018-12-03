import {Component, ViewChild} from '@angular/core';
import { NavController } from 'ionic-angular';
import { RestProvider } from "../../providers/rest/rest";
import {LoginPage} from "../login/login";
import {ContactPage} from "../contact/contact";

@Component({
  selector: 'page-about',
  templateUrl: 'about.html'
})
export class AboutPage {

  @ViewChild('gig') gig;
  @ViewChild('city') city;
  gigList: any;

  constructor(public navCtrl: NavController, public restProvider: RestProvider) {

  }

  searchGigs() {
    // Try and search for gigs through the django api
    // If successful populate list in template
    try {
      this.restProvider.searchGigs(this.gig.value, this.city.value)
        .then(data => {
          this.gigList = data;
          console.log(this.gigList);
        });
    }
    catch (e) {
      console.log(e)
    }
  }

  locateVenue(venueId){
    // Try and search for venue information
    // If successful push to map tab
    try {
      this.restProvider.venueInfo(venueId)
        .then(data => {
          this.navCtrl.push(ContactPage, {venue: data});
          console.log(data);
        });
    }
    catch (e) {
      console.log(e)
    }
  }

}
