class Trie
    clusterSize: 3

    constructor: (cluster) ->
        @children = {}
        @data = null
        @cluster = cluster

    newCluster: -> (null for i in [1..@clusterSize])

    insert: (path, data) ->
        node = @
        cluster = @newCluster()
        data or= path
        for item in path
            cluster = (cluster.concat item)[-@clusterSize..]
            if not node.children[item]
                node.children[item] = new Trie(cluster)
            node = node.children[item]

        node.data = data

    search: (q) ->
        results = @searchRecursive q[0], q[1..], [], [], @newCluster()
        results.sort (a, b) ->
            b.similarity - a.similarity
        return results

    searchRecursive: (head, tail, results, clusters, cluster) ->
        head = head.toLowerCase() unless not head
        tail = tail.toLowerCase() unless not tail
        for item, node of @children
            if not tail and node.data
                results.push
                    data: node.data
                    similarity: clusters.length

            if item == head
                newCluster = (cluster[..].concat head)[-@clusterSize..]
                if node.cluster.join() == newCluster.join()
                    newClusters = clusters[..].concat [newCluster]
                else
                    newClusters = clusters
                [newHead, newTail] = [tail[0], tail[1..]]
                node.searchRecursive newHead, newTail, results, newClusters, newCluster
            else
                node.searchRecursive head, tail, results, clusters, cluster

        return results


root = exports ? this
root.Trie = Trie
