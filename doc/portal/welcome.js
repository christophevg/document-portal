var Welcome = {
  template: `
<div>
  <h1>Welcome</h1>

  <p>
  
    Navigate to any of the document types to find your documents. Actions
    behind the scenes will be logged here. Try visiting "all" documents and
    returning here to see the document gateway in action.
  
  </p>
  
  <p>
  
    You are user "x" and information about documents will be restricted to
    those that you own. E.g. document 4 is owned by user "y".
  
  </p>

  <h2>Log</h2>
  <span class="grey--text">Most recent entry on top.</span>
  <v-expansion-panel popout>
    <v-expansion-panel-content v-for="(message, i) in messages" :key="i" hide-actions>
      <v-layout slot="header" align-left row spacer>
        <div>
          <span class="grey--text">{{ message.when | formatDate }}</span>
          <br>
          <span><b>[{{ message.reporter }}] - {{ message.message }}</b></span>
          <br>
          <div v-if="message.arguments" v-html="$options.filters.syntaxHighlight(message.arguments, 250)"></div>
        </div>
      </v-layout>
    </v-expansion-panel-content> 
  </v-expansion-panel>

</div>
`,
  computed: {
    messages : function() {
      return store.getters.logs;
    }
  }
};

store.registerModule("Welcome", {
  state: {
    log: []
  },
  mutations: {
    log: function(state, msg) {
      msg["when"] = Date.now()
      state.log.unshift(msg);
    },
  },
  getters: {
    logs: function(state) {
      return state.log;
    }
  }
});

// log to console setup

socket.on("log", function(msg){
  store.commit("log", msg);
});
