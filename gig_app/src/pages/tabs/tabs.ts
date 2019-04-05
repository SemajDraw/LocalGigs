import { Component } from '@angular/core';
import { SearchPage } from '../search/search';
import { MapPage } from '../map/map';
import { ProfilePage } from '../profile/profile';

@Component({
  templateUrl: 'tabs.html'
})
export class TabsPage {

  tab1Root = SearchPage;
  tab2Root = ProfilePage;
  tab3Root = MapPage;

  constructor() {

  }
}
