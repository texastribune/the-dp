// Generated by CoffeeScript 1.3.3
(function() {
  var Trie, root;

  Trie = (function() {

    Trie.prototype.clusterSize = 3;

    function Trie(cluster) {
      this.children = {};
      this.data = null;
      this.cluster = cluster;
    }

    Trie.prototype.newCluster = function() {
      var i, _i, _ref, _results;
      _results = [];
      for (i = _i = 1, _ref = this.clusterSize; 1 <= _ref ? _i <= _ref : _i >= _ref; i = 1 <= _ref ? ++_i : --_i) {
        _results.push(null);
      }
      return _results;
    };

    Trie.prototype.insert = function(path, data) {
      var cluster, item, node, _i, _len;
      node = this;
      cluster = this.newCluster();
      data || (data = path);
      for (_i = 0, _len = path.length; _i < _len; _i++) {
        item = path[_i];
        cluster = (cluster.concat(item)).slice(-this.clusterSize);
        if (!node.children[item]) {
          node.children[item] = new Trie(cluster);
        }
        node = node.children[item];
      }
      return node.data = data;
    };

    Trie.prototype.search = function(q) {
      var results;
      results = this.searchRecursive(q[0], q.slice(1), [], [], this.newCluster());
      results.sort(function(a, b) {
        return b.similarity - a.similarity;
      });
      return results;
    };

    Trie.prototype.searchRecursive = function(head, tail, results, clusters, cluster) {
      var item, newCluster, newClusters, newHead, newTail, node, _ref, _ref1;
      if (!!head) {
        head = head.toLowerCase();
      }
      if (!!tail) {
        tail = tail.toLowerCase();
      }
      _ref = this.children;
      for (item in _ref) {
        node = _ref[item];
        if (!tail && node.data) {
          results.push({
            data: node.data,
            similarity: clusters.length
          });
        }
        if (item === head) {
          newCluster = (cluster.slice(0).concat(head)).slice(-this.clusterSize);
          if (node.cluster.join() === newCluster.join()) {
            newClusters = clusters.slice(0).concat([newCluster]);
          } else {
            newClusters = clusters;
          }
          _ref1 = [tail[0], tail.slice(1)], newHead = _ref1[0], newTail = _ref1[1];
          node.searchRecursive(newHead, newTail, results, newClusters, newCluster);
        } else {
          node.searchRecursive(head, tail, results, clusters, cluster);
        }
      }
      return results;
    };

    return Trie;

  })();

  root = typeof exports !== "undefined" && exports !== null ? exports : this;

  root.Trie = Trie;

}).call(this);
