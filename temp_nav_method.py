    def on_nav_change(self, e):
        # Switch content based on selected navigation index
        index = self.nav_bar.selected_index
        
        if index == 0:
            self.content_area.content = self.build_guest_list_tab()
        elif index == 1:
            self.content_area.content = self.build_party_details_tab()
        elif index == 2:
            self.content_area.content = self.build_cloud_rsvps_tab()
        elif index == 3:
            self.content_area.content = self.build_broadcasts_tab()
        
        self.page.update()
