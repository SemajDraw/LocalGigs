import {Component, ViewChild} from '@angular/core';
import { NavController } from 'ionic-angular';
import { RestProvider } from "../../providers/rest/rest";
import { Events } from "ionic-angular";


@Component({
  selector: 'page-search',
  templateUrl: 'search.html'
})
export class SearchPage {

  @ViewChild('search') search;
  gigList: any;

  constructor(public navCtrl: NavController, public restProvider: RestProvider,
              public events: Events) {

  }

  ionViewDidLoad() {
    this.getMusicEvents();
  }

  getMusicEvents() {
    try {
      this.restProvider.searchEvents("music")
        .then(data => {
          this.gigList = data;
          console.log(this.gigList);
        });
    }
    catch (e) {
      console.log(e)
    }
  }

  getRecommendedEvents() {
    try {
      this.restProvider.getRecommendedEvents()
        .then(data => {
          this.gigList = data;
          console.log(this.gigList);
        });
    }
    catch (e) {
      console.log(e)
    }
  }

  searchGigs() {
    // Try and search for gigs through the django api
    // If successful populate list in template
    try {
      this.restProvider.searchEvents(this.search.value)
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

}
