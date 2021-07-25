var Viewer = {
  template : `
 <v-card>
    <v-card-title>
      My Documents
      <v-spacer></v-spacer>
      <v-text-field
        v-model="search"
        append-icon="search"
        label="Search"
        single-line
        hide-details
      ></v-text-field>
    </v-card-title>
  <v-data-table
    :headers="headers"
    :items="documents"
    :items-per-page="5"
    class="elevation-1"
    :loading="loading"
    select-all
    :search="search"
  >
    <template slot="items" slot-scope="props">
      <td width="1%">
        <v-checkbox
          v-model="props.selected"
          primary
          hide-details
        ></v-checkbox>
      </td>
      <td v-for="prop in properties" :align="alignment(prop)" :width="width(prop)">
        {{ props.item[prop] }}
      </td>
      <td align="right" width="1%">
        <v-btn icon :href="'/documents/' + props.item.guid" target="_blank">
          <v-icon>description</v-icon>
        </v-btn>
        </td>
    </template>
  </v-data-table>
</v-card>
`,
  computed: {
    headers: function() {
      var heads = store.getters.headers(this.$route.path.slice(1));
      return heads.concat({ text: "", align:"center", value: 'name', sortable: false });
    },
    properties: function() {
      var heads = store.getters.headers(this.$route.path.slice(1));
      return heads.map(function(head) {
        return head.value;
      });
    },
    alignment: function() {
      return function(prop) {
        var heads = store.getters.headers(this.$route.path.slice(1));
        return heads.filter(function(head) {
          return head.value == prop;
        })[0]["align"];
      }
    },
    width: function() {
      return function(prop) {
        var heads = store.getters.headers(this.$route.path.slice(1));
        return heads.filter(function(head) {
          return head.value == prop;
        })[0]["width"];
      }
    },
    documents : function() {
      return store.getters.documents;
    },
    download: function() {
      return function(guid) {
        return "/documents/" + guid;
      }
    },
    loading: function() {
      return store.getters.loading;
    }
  },
  data: function() {
    return {
      search: ''
    }
  },
  // initial selection
  created: function(){
    store.dispatch("handleTypeChange", this.$route.path.slice(1));
  },
  // changed selection
  watch:{
    $route: function(to, from) {
      store.dispatch("handleTypeChange", to.path.slice(1));
    }
  } 
};

function add_type(type) {
  // add route and navigation entry
  router.addRoutes([
    { path: "/"+ type, component: Viewer },
  ])
  app.sections.push({
    icon  : "description",
    text  : type,
    path  : "/" + type   
  });
}

// set up page specific part in the store

store.registerModule("Viewer", {
  state: {
    log: [],
    types: [],
    documents: [],
    loading: false
  },
  mutations: {
    log: function(state, msg) {
      now = Date.now()
      msg["log"]["commit"] = now;
      msg["log"]["received"] = Math.round(msg["log"]["received"] + state.skew);
      msg["elapsed"] = now - msg["log"]["received"];
      state.log.unshift({ when: new Date(), body: msg });
    },
    types: function(state, types) {
      state.types = types;
      for( var type in types ) {
        add_type(type);
      }
      // on reload a previous path might be present => activate it again
      if(app.$route.path != "/") {
        router.push({ path: decodeURIComponent(app.$route.path) });
      }
    },
    documents: function(state, documents) {
      for(var doc in documents) {
        state.documents.push(documents[doc]);
      }
      state.loading = false;
    },
    reload: function(state) {
      state.documents.splice(0, state.documents.length);      
      state.loading = true;
    }
  },
  getters: {
    logs: function(state) {
      return state.log;
    },
    headers: function(state) {
      return function(type) {
        return state.types[type]["headers"];
      }
    },
    documents: function(state) {
      return state.documents;
    },
    loading: function(state) {
      return state.loading;a
    }
  },
  actions: {
    handleTypeChange: function(context, type) {
      store.commit("reload");
      $.ajax({
        url: "/documents?type="+type,
        type: "get",
        success: function(documents) {
          console.log(documents);
          store.commit("documents", documents );
        },
        error: function(response) {
          app.$notify({
            group: "notifications",
            title: "Could not fetch documents...",
            text:  response.responseText,
            type:  "warn",
            duration: 10000
          });
        }
      });
    }
  }
});

// log to console setup

socket.on("log", function(msg){
  console.log(msg);
});

// load types to populate menu

$.ajax({
  url: "/meta/types",
  type: "get",
  success: function(response) {
    store.commit("types", response);
  },
  error: function(response) {
    app.$notify({
      group: "notifications",
      title: "Could not refresh types...",
      text:  response.responseText,
      type:  "warn",
      duration: 10000
    });
  }
});